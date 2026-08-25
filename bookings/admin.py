from django.contrib import admin

from bookings.models import (
    Appointment,
    Customer,
    Practitioner,
    PractitionerSchedule,
    PractitionerService,
    ScheduleException,
    Service,
    ServiceSchedule,
)


class PractitionerServiceInline(admin.TabularInline):
    model = PractitionerService
    extra = 1


class PractitionerScheduleInline(admin.TabularInline):
    model = PractitionerSchedule
    extra = 1


class ServiceScheduleInline(admin.TabularInline):
    model = ServiceSchedule
    extra = 0
    fields = ('day_of_week', 'start_time', 'end_time', 'is_unavailable')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'duration_minutes',
        'buffer_minutes',
        'price',
        'is_active',
        'sort_order',
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceScheduleInline]


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ('service', 'day_of_week', 'start_time', 'end_time', 'is_unavailable')
    list_filter = ('day_of_week', 'is_unavailable', 'service')
    search_fields = ('service__name',)


@admin.register(Practitioner)
class PractitionerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [PractitionerServiceInline, PractitionerScheduleInline]


@admin.register(PractitionerSchedule)
class PractitionerScheduleAdmin(admin.ModelAdmin):
    list_display = ('practitioner', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'practitioner')
    search_fields = ('practitioner__first_name', 'practitioner__last_name')


@admin.register(ScheduleException)
class ScheduleExceptionAdmin(admin.ModelAdmin):
    list_display = ('exception_date', 'practitioner', 'is_closed', 'start_time', 'end_time', 'reason')
    list_filter = ('is_closed', 'exception_date')
    search_fields = ('reason', 'practitioner__first_name', 'practitioner__last_name')
    date_hierarchy = 'exception_date'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'start_datetime',
        'customer',
        'service',
        'practitioner',
        'status',
        'source',
    )
    list_filter = (
        'status',
        'service',
        'practitioner',
        'source',
    )
    search_fields = (
        'customer__first_name',
        'customer__last_name',
        'customer__email',
        'confirmation_token',
    )
    readonly_fields = (
        'confirmation_token',
        'created_at',
        'updated_at',
    )
    fieldsets = (
        (None, {
            'fields': (
                'customer',
                'service',
                'practitioner',
                'start_datetime',
                'end_datetime',
                'status',
                'source',
                'customer_notes',
                'internal_notes',
                'confirmation_token',
            ),
        }),
        ('Cancellation', {
            'fields': ('cancelled_at', 'cancellation_reason'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    date_hierarchy = 'start_datetime'
