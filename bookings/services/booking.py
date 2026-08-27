from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from bookings.models import Appointment, Customer, Service
from bookings.services.availability import (
    SLOT_HOLDING_STATUSES,
    get_slot_capacity,
    is_slot_available,
)
from bookings.services.google_calendar import create_calendar_event
from bookings.services.notifications import (
    DATE_FORMAT,
    TIME_FORMAT,
    send_booking_cancellation,
    send_booking_confirmation,
    send_booking_rejection,
    send_booking_request,
    send_booking_update,
)


DEFAULT_REJECT_MESSAGE = (
    'This slot is already booked. Kindly book another slot.'
)


class BookingError(Exception):
    pass


class SlotUnavailableError(BookingError):
    pass


class ServiceUnavailableError(BookingError):
    pass


class PractitionerUnavailableError(BookingError):
    pass


def _reload(appointment_id: int) -> Appointment:
    return Appointment.objects.select_related(
        'customer', 'service', 'practitioner'
    ).get(pk=appointment_id)


@transaction.atomic
def create_appointment(
    *,
    service_id: int,
    start_datetime,
    customer_data: dict,
    practitioner_id: int | None = None,
    customer_notes: str = '',
    source: str = Appointment.Source.ONLINE,
    duration_minutes: int | None = None,
) -> Appointment:
    try:
        service = Service.objects.get(pk=service_id, is_active=True)
    except Service.DoesNotExist as exc:
        raise ServiceUnavailableError('Selected service is not available.') from exc

    try:
        length = service.resolve_duration(duration_minutes)
    except ValueError as exc:
        raise BookingError(str(exc)) from exc

    slot = is_slot_available(service, start_datetime, duration_minutes=length)
    if slot is None:
        raise SlotUnavailableError('The selected time slot is no longer available.')

    occupied_end = slot.start_datetime + timedelta(
        minutes=length + service.buffer_minutes
    )

    # Lock the overlapping appointments so concurrent bookings cannot exceed
    # this service's slot capacity.
    overlapping = list(
        Appointment.objects.select_for_update().filter(
            service=service,
            status__in=[*SLOT_HOLDING_STATUSES, Appointment.Status.REJECTED],
            start_datetime__lt=occupied_end,
            end_datetime__gt=slot.start_datetime,
        )
    )
    if any(item.status == Appointment.Status.REJECTED for item in overlapping):
        raise SlotUnavailableError('This time is fully booked. Please choose another time.')
    held = [item for item in overlapping if item.status in SLOT_HOLDING_STATUSES]
    if len(held) >= get_slot_capacity(service):
        raise SlotUnavailableError('This time is fully booked. Please choose another time.')

    customer = Customer.objects.create(
        first_name=customer_data['first_name'].strip(),
        last_name=customer_data['last_name'].strip(),
        email=customer_data['email'].strip().lower(),
        phone=customer_data['phone'].strip(),
    )

    appointment = Appointment.objects.create(
        customer=customer,
        service=service,
        practitioner=None,
        start_datetime=slot.start_datetime,
        end_datetime=slot.end_datetime,
        status=Appointment.Status.PENDING,
        customer_notes=customer_notes.strip(),
        source=source,
    )

    appointment_id = appointment.pk

    def _notify():
        send_booking_request(_reload(appointment_id))

    transaction.on_commit(_notify)
    return appointment


@transaction.atomic
def approve_appointment(appointment: Appointment) -> Appointment:
    if appointment.status == Appointment.Status.CONFIRMED:
        return appointment
    if appointment.status != Appointment.Status.PENDING:
        raise BookingError('Only pending requests can be approved.')

    appointment.status = Appointment.Status.CONFIRMED
    appointment.save(update_fields=['status', 'updated_at'])
    appointment_id = appointment.pk

    def _notify():
        confirmed = _reload(appointment_id)
        send_booking_confirmation(confirmed)
        create_calendar_event(confirmed)

    transaction.on_commit(_notify)
    return appointment


@transaction.atomic
def reject_appointment(appointment: Appointment, reason: str = '') -> Appointment:
    if appointment.status == Appointment.Status.REJECTED:
        return appointment
    if appointment.status != Appointment.Status.PENDING:
        raise BookingError('Only pending requests can be rejected.')

    message = (reason or '').strip() or DEFAULT_REJECT_MESSAGE
    appointment.status = Appointment.Status.REJECTED
    appointment.cancelled_at = timezone.now()
    appointment.cancellation_reason = message
    appointment.save(
        update_fields=['status', 'cancelled_at', 'cancellation_reason', 'updated_at']
    )
    appointment_id = appointment.pk
    transaction.on_commit(lambda: send_booking_rejection(_reload(appointment_id)))
    return appointment


@transaction.atomic
def cancel_appointment(appointment: Appointment, reason: str = '') -> Appointment:
    if appointment.status in {Appointment.Status.CANCELLED, Appointment.Status.REJECTED}:
        return appointment
    if appointment.status not in {Appointment.Status.PENDING, Appointment.Status.CONFIRMED}:
        raise BookingError('Only active appointments can be cancelled.')

    was_confirmed = appointment.status == Appointment.Status.CONFIRMED
    appointment.status = Appointment.Status.CANCELLED
    appointment.cancelled_at = timezone.now()
    appointment.cancellation_reason = reason.strip()
    appointment.save(
        update_fields=['status', 'cancelled_at', 'cancellation_reason', 'updated_at']
    )
    appointment_id = appointment.pk
    if was_confirmed:
        transaction.on_commit(lambda: send_booking_cancellation(_reload(appointment_id)))
    else:
        transaction.on_commit(lambda: send_booking_rejection(_reload(appointment_id)))
    return appointment


def _snapshot(appointment: Appointment) -> dict:
    start_local = timezone.localtime(appointment.start_datetime)
    return {
        'service_name': appointment.service.name,
        'appointment_date': start_local.strftime(DATE_FORMAT),
        'appointment_time': start_local.strftime(TIME_FORMAT),
    }


@transaction.atomic
def update_appointment(
    appointment: Appointment,
    *,
    start_datetime=None,
    service_id: int | None = None,
    practitioner_id: int | None = None,
    status: str | None = None,
    customer_message: str = '',
    notify: bool = True,
) -> Appointment:
    """Change an existing booking and email the customer the updated details."""
    if appointment.status in {Appointment.Status.CANCELLED, Appointment.Status.REJECTED}:
        raise BookingError('Cancelled appointments cannot be updated.')

    previous = _snapshot(appointment)
    update_fields = ['updated_at']

    if service_id is not None and service_id != appointment.service_id:
        try:
            service = Service.objects.get(pk=service_id, is_active=True)
        except Service.DoesNotExist as exc:
            raise ServiceUnavailableError('Selected service is not available.') from exc
        appointment.service = service
        update_fields.append('service')

    if start_datetime is not None and start_datetime != appointment.start_datetime:
        slot = is_slot_available(
            appointment.service,
            start_datetime,
            duration_minutes=appointment.duration_minutes,
        )
        if slot is None:
            raise SlotUnavailableError('The selected time slot is no longer available.')
        appointment.start_datetime = slot.start_datetime
        appointment.end_datetime = slot.end_datetime
        update_fields.extend(['start_datetime', 'end_datetime'])

    if practitioner_id is not None:
        appointment.practitioner_id = practitioner_id or None
        update_fields.append('practitioner')

    if status is not None and status != appointment.status:
        appointment.status = status
        update_fields.append('status')

    appointment.save(update_fields=update_fields)
    if notify and appointment.status == Appointment.Status.CONFIRMED:
        appointment_id = appointment.pk
        previous_copy = previous
        message = customer_message
        transaction.on_commit(
            lambda: send_booking_update(
                _reload(appointment_id),
                previous=previous_copy,
                message=message,
            )
        )
    return appointment
