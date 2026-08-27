from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.utils import timezone

from bookings.models import Appointment, ScheduleException, Service, ServiceSchedule
from website.visit import clinic_hours_bounds

SLOT_INCREMENT_MINUTES = 15
DEFAULT_SLOT_CAPACITY = 5


def get_slot_capacity(service: Service | None = None) -> int:
    """How many patients may book the same time slot for this service."""
    if service is not None:
        return max(1, int(getattr(service, 'slot_capacity', 1) or 1))
    return int(getattr(settings, 'BOOKING_SLOT_CAPACITY', DEFAULT_SLOT_CAPACITY))


@dataclass(frozen=True)
class AvailableSlot:
    start_datetime: datetime
    end_datetime: datetime
    available_spaces: int
    practitioner_id: int | None = None
    practitioner_name: str = ''


def _combine(target_date: date, clock_time: time) -> datetime:
    naive = datetime.combine(target_date, clock_time)
    return timezone.make_aware(naive, timezone.get_current_timezone())


def _get_service_windows(service: Service, target_date: date) -> list[tuple[time, time]]:
    """Booking windows for a service on a date from ServiceSchedule (or clinic hours)."""
    clinic_closed = ScheduleException.objects.filter(
        practitioner__isnull=True,
        exception_date=target_date,
        is_closed=True,
    ).exists()
    if clinic_closed:
        return []

    day_of_week = target_date.weekday()
    clinic_opens, clinic_closes = clinic_hours_bounds(day_of_week)
    if clinic_opens is None or clinic_closes is None:
        return []

    if ServiceSchedule.objects.filter(service=service).exists():
        row = ServiceSchedule.objects.filter(
            service=service,
            day_of_week=day_of_week,
        ).first()
        if row is None or row.is_unavailable:
            return []
        if row.start_time and row.end_time and row.start_time < row.end_time:
            start = max(row.start_time, clinic_opens)
            end = min(row.end_time, clinic_closes)
            if start >= end:
                return []
            return [(start, end)]
        return []

    # No service schedule configured yet — fall back to full clinic hours.
    return [(clinic_opens, clinic_closes)]


SLOT_HOLDING_STATUSES = (
    Appointment.Status.PENDING,
    Appointment.Status.CONFIRMED,
)


def _overlapping_appointments(start: datetime, end: datetime, service: Service | None = None):
    queryset = Appointment.objects.filter(
        start_datetime__lt=end,
        end_datetime__gt=start,
    )
    if service is not None:
        queryset = queryset.filter(service=service)
    return queryset


def count_overlapping_appointments(
    start: datetime,
    end: datetime,
    service: Service | None = None,
) -> int:
    """Active appointments that overlap the given window."""
    return _overlapping_appointments(start, end, service).filter(
        status__in=SLOT_HOLDING_STATUSES,
    ).count()


def has_rejected_overlap(
    start: datetime,
    end: datetime,
    service: Service | None = None,
) -> bool:
    """True when staff rejected a booking that still occupies this window."""
    return _overlapping_appointments(start, end, service).filter(
        status=Appointment.Status.REJECTED,
    ).exists()


def _iter_slot_starts(window_start: time, window_end: time, step_minutes: int):
    current = datetime.combine(date.today(), window_start)
    end = datetime.combine(date.today(), window_end)
    step = timedelta(minutes=step_minutes)
    while current + step <= end:
        yield current.time()
        current += step


def compute_slots(
    service: Service,
    target_date: date,
    practitioner_id: int | None = None,
    duration_minutes: int | None = None,
) -> list[AvailableSlot]:
    windows = _get_service_windows(service, target_date)
    if not windows:
        return []

    try:
        length = service.resolve_duration(duration_minutes)
    except ValueError:
        return []

    capacity = get_slot_capacity(service)
    slot_duration = timedelta(minutes=length)
    buffer_duration = timedelta(minutes=service.buffer_minutes)
    occupied_duration = slot_duration + buffer_duration
    now = timezone.now()

    slots: list[AvailableSlot] = []
    for window_start, window_end in windows:
        window_end_dt = _combine(target_date, window_end)
        for slot_start_time in _iter_slot_starts(
            window_start,
            window_end,
            SLOT_INCREMENT_MINUTES,
        ):
            start = _combine(target_date, slot_start_time)
            end = start + slot_duration
            occupied_end = start + occupied_duration

            if occupied_end > window_end_dt:
                continue
            if start <= now:
                continue
            if has_rejected_overlap(start, occupied_end, service=service):
                continue

            taken = count_overlapping_appointments(start, occupied_end, service=service)
            available = capacity - taken
            if available <= 0:
                continue

            slots.append(
                AvailableSlot(
                    start_datetime=start,
                    end_datetime=end,
                    available_spaces=available,
                )
            )

    slots.sort(key=lambda slot: slot.start_datetime)
    return slots


def is_slot_available(
    service: Service,
    start_datetime: datetime,
    practitioner_id: int | None = None,
    duration_minutes: int | None = None,
) -> AvailableSlot | None:
    target_date = timezone.localtime(start_datetime).date()
    for slot in compute_slots(
        service,
        target_date,
        duration_minutes=duration_minutes,
    ):
        if slot.start_datetime == start_datetime:
            return slot
    return None
