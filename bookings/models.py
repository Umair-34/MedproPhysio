import uuid

from django.db import models
from django.db.models import Q


class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    duration_options = models.JSONField(
        default=list,
        blank=True,
        help_text='Extra bookable lengths in minutes, e.g. [30, 60]. The default length is still duration_minutes.',
    )
    buffer_minutes = models.PositiveIntegerField(default=10)
    slot_capacity = models.PositiveIntegerField(
        default=1,
        help_text='How many patients can book the same start time. Use 1 for massage, chiropractic, and kinesiology; higher for physiotherapy.',
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def allowed_durations(self) -> list[int]:
        values = []
        for raw in self.duration_options or []:
            try:
                minutes = int(raw)
            except (TypeError, ValueError):
                continue
            if minutes > 0:
                values.append(minutes)
        if self.duration_minutes:
            values.append(int(self.duration_minutes))
        return sorted(set(values))

    def resolve_duration(self, requested=None) -> int:
        allowed = self.allowed_durations()
        if not allowed:
            raise ValueError('This service has no bookable length.')
        if requested in (None, ''):
            default = int(self.duration_minutes)
            return default if default in allowed else allowed[0]
        try:
            minutes = int(requested)
        except (TypeError, ValueError) as exc:
            raise ValueError('Choose a valid appointment length.') from exc
        if minutes not in allowed:
            raise ValueError('Choose a valid appointment length.')
        return minutes


class ServiceSchedule(models.Model):
    """Weekly booking windows for a service (e.g. Massage Mon–Fri 8:00–10:00)."""

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='schedules',
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_unavailable = models.BooleanField(
        default=False,
        help_text='When checked, this service cannot be booked on this weekday.',
    )

    class Meta:
        ordering = ['service', 'day_of_week']
        indexes = [
            models.Index(fields=['service', 'day_of_week']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'day_of_week'],
                name='unique_service_day_schedule',
            ),
        ]

    def __str__(self):
        day = self.get_day_of_week_display()
        if self.is_unavailable:
            return f'{self.service} — {day} (unavailable)'
        if self.start_time and self.end_time:
            return (
                f'{self.service} — {day} '
                f'{self.start_time:%H:%M}–{self.end_time:%H:%M}'
            )
        return f'{self.service} — {day}'


class Practitioner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='practitioners/', blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    services = models.ManyToManyField(
        Service,
        through='PractitionerService',
        related_name='practitioners',
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return str(self)


class PractitionerService(models.Model):
    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        related_name='practitioner_services',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='practitioner_services',
    )

    class Meta:
        unique_together = ('practitioner', 'service')

    def __str__(self):
        return f'{self.practitioner} — {self.service}'


class PractitionerSchedule(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        related_name='schedules',
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day_of_week', 'start_time']
        indexes = [
            models.Index(fields=['practitioner', 'day_of_week']),
        ]

    def __str__(self):
        return (
            f'{self.practitioner} — {self.get_day_of_week_display()} '
            f'{self.start_time:%H:%M}–{self.end_time:%H:%M}'
        )


class ScheduleException(models.Model):
    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        related_name='schedule_exceptions',
        null=True,
        blank=True,
        help_text='Leave blank for clinic-wide closures.',
    )
    exception_date = models.DateField()
    is_closed = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['exception_date']
        indexes = [
            models.Index(fields=['exception_date']),
            models.Index(fields=['practitioner', 'exception_date']),
        ]

    def __str__(self):
        target = self.practitioner or 'Clinic-wide'
        if self.is_closed:
            return f'{target} closed on {self.exception_date}'
        return (
            f'{target} special hours on {self.exception_date} '
            f'{self.start_time:%H:%M}–{self.end_time:%H:%M}'
        )


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return str(self)


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'
        NO_SHOW = 'no_show', 'No show'

    class Source(models.TextChoices):
        ONLINE = 'online', 'Online'
        PHONE = 'phone', 'Phone'
        WALK_IN = 'walk_in', 'Walk-in'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='appointments',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments',
    )
    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.SET_NULL,
        related_name='appointments',
        null=True,
        blank=True,
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    customer_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.ONLINE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['start_datetime', 'status']),
            models.Index(fields=['confirmation_token']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['practitioner', 'start_datetime'],
                condition=Q(status__in=['confirmed', 'pending']),
                name='unique_active_practitioner_slot',
            ),
        ]

    def __str__(self):
        practitioner_name = self.practitioner or 'Unassigned'
        return (
            f'{self.customer} — {self.service} with {practitioner_name} '
            f'at {self.start_datetime:%Y-%m-%d %H:%M}'
        )

    @property
    def is_active(self):
        return self.status in {self.Status.PENDING, self.Status.CONFIRMED}

    @property
    def duration_minutes(self) -> int:
        delta = self.end_datetime - self.start_datetime
        return max(1, int(delta.total_seconds() // 60))
