from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from bookings.models import Appointment, Customer, Service
from bookings.services.availability import get_slot_capacity, is_slot_available
from bookings.services.google_calendar import create_calendar_event
from bookings.services.notifications import (
    send_booking_cancellation,
    send_booking_confirmation,
)


class BookingError(Exception):
    pass


class SlotUnavailableError(BookingError):
    pass


class ServiceUnavailableError(BookingError):
    pass


class PractitionerUnavailableError(BookingError):
    pass


@transaction.atomic
def create_appointment(
    *,
    service_id: int,
    start_datetime,
    customer_data: dict,
    practitioner_id: int | None = None,
    customer_notes: str = '',
    source: str = Appointment.Source.ONLINE,
) -> Appointment:
    try:
        service = Service.objects.get(pk=service_id, is_active=True)
    except Service.DoesNotExist as exc:
        raise ServiceUnavailableError('Selected service is not available.') from exc

    slot = is_slot_available(service, start_datetime)
    if slot is None:
        raise SlotUnavailableError('The selected time slot is no longer available.')

    occupied_end = slot.start_datetime + timedelta(
        minutes=service.duration_minutes + service.buffer_minutes
    )

    # Lock the overlapping appointments so concurrent bookings cannot exceed
    # the per-slot capacity (for example, 5 patients on the same 5 PM slot).
    overlapping = list(
        Appointment.objects.select_for_update().filter(
            service=service,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
            start_datetime__lt=occupied_end,
            end_datetime__gt=slot.start_datetime,
        )
    )
    if len(overlapping) >= get_slot_capacity():
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
        status=Appointment.Status.CONFIRMED,
        customer_notes=customer_notes.strip(),
        source=source,
    )

    # Send emails and create the calendar event only after the booking has
    # been committed, so notifications never reference a rolled-back record.
    def _notify():
        send_booking_confirmation(appointment)
        create_calendar_event(appointment)

    transaction.on_commit(_notify)
    return appointment


@transaction.atomic
def cancel_appointment(appointment: Appointment, reason: str = '') -> Appointment:
    if appointment.status == Appointment.Status.CANCELLED:
        return appointment
    if appointment.status not in {Appointment.Status.PENDING, Appointment.Status.CONFIRMED}:
        raise BookingError('Only active appointments can be cancelled.')

    appointment.status = Appointment.Status.CANCELLED
    appointment.cancelled_at = timezone.now()
    appointment.cancellation_reason = reason.strip()
    appointment.save(
        update_fields=['status', 'cancelled_at', 'cancellation_reason', 'updated_at']
    )
    transaction.on_commit(lambda: send_booking_cancellation(appointment))
    return appointment
