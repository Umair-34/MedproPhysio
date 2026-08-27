from django.db import migrations


def add_psychology_counselling_service(apps, schema_editor):
    Service = apps.get_model('bookings', 'Service')
    Practitioner = apps.get_model('bookings', 'Practitioner')
    PractitionerService = apps.get_model('bookings', 'PractitionerService')

    service, _created = Service.objects.get_or_create(
        slug='psychology-counselling',
        defaults={
            'name': 'Psychology Counselling',
            'description': 'Confidential counselling for stress, anxiety, and recovery related mental wellness.',
            'duration_minutes': 50,
            'buffer_minutes': 10,
            'sort_order': 6,
            'is_active': True,
        },
    )
    practitioner_id = (
        PractitionerService.objects.filter(service__slug='physiotherapy')
        .values_list('practitioner_id', flat=True)
        .first()
    )
    practitioner = None
    if practitioner_id:
        practitioner = Practitioner.objects.filter(pk=practitioner_id).first()
    if practitioner is None:
        practitioner = Practitioner.objects.first()
    if practitioner:
        PractitionerService.objects.get_or_create(practitioner=practitioner, service=service)


def remove_psychology_counselling_service(apps, schema_editor):
    Service = apps.get_model('bookings', 'Service')
    Service.objects.filter(slug='psychology-counselling').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_add_service_schedule'),
    ]

    operations = [
        migrations.RunPython(add_psychology_counselling_service, remove_psychology_counselling_service),
    ]
