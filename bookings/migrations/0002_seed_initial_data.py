from datetime import time

from django.db import migrations


def seed_data(apps, schema_editor):
    Service = apps.get_model('bookings', 'Service')
    Practitioner = apps.get_model('bookings', 'Practitioner')
    PractitionerService = apps.get_model('bookings', 'PractitionerService')
    PractitionerSchedule = apps.get_model('bookings', 'PractitionerSchedule')

    services = [
        {
            'name': 'Massage',
            'slug': 'massage',
            'description': 'Therapeutic and relaxation massage treatments.',
            'duration_minutes': 60,
            'buffer_minutes': 10,
            'sort_order': 1,
        },
        {
            'name': 'Physiotherapy',
            'slug': 'physiotherapy',
            'description': 'Assessment and treatment for injury, pain, and mobility.',
            'duration_minutes': 45,
            'buffer_minutes': 10,
            'sort_order': 2,
        },
        {
            'name': 'Chiropractic',
            'slug': 'chiropractic',
            'description': 'Spinal and musculoskeletal alignment care.',
            'duration_minutes': 30,
            'buffer_minutes': 10,
            'sort_order': 3,
        },
        {
            'name': 'Acupuncture',
            'slug': 'acupuncture',
            'description': 'Traditional acupuncture for pain relief and wellness.',
            'duration_minutes': 45,
            'buffer_minutes': 10,
            'sort_order': 4,
        },
        {
            'name': 'Kinesiology',
            'slug': 'kinesiology',
            'description': 'Movement-based therapy and exercise rehabilitation.',
            'duration_minutes': 45,
            'buffer_minutes': 10,
            'sort_order': 5,
        },
    ]

    service_objects = {}
    for service_data in services:
        service_objects[service_data['slug']] = Service.objects.create(**service_data)

    practitioners = [
        {
            'first_name': 'Sarah',
            'last_name': 'Mitchell',
            'email': 'sarah.mitchell@medprophysio.example',
            'bio': 'Registered physiotherapist with a focus on sports injury recovery.',
            'services': ['physiotherapy', 'kinesiology'],
        },
        {
            'first_name': 'James',
            'last_name': 'Chen',
            'email': 'james.chen@medprophysio.example',
            'bio': 'Chiropractor experienced in spinal and postural care.',
            'services': ['chiropractic'],
        },
        {
            'first_name': 'Emma',
            'last_name': 'Wilson',
            'email': 'emma.wilson@medprophysio.example',
            'bio': 'Remedial massage therapist and acupuncture practitioner.',
            'services': ['massage', 'acupuncture'],
        },
        {
            'first_name': 'Liam',
            'last_name': 'Patel',
            'email': 'liam.patel@medprophysio.example',
            'bio': 'Kinesiologist supporting strength and mobility programmes.',
            'services': ['kinesiology', 'physiotherapy'],
        },
    ]

    weekday_hours = (time(8, 30), time(17, 30))
    weekdays = range(5)

    for practitioner_data in practitioners:
        service_slugs = practitioner_data.pop('services')
        practitioner = Practitioner.objects.create(**practitioner_data)
        for slug in service_slugs:
            PractitionerService.objects.create(
                practitioner=practitioner,
                service=service_objects[slug],
            )
        for day in weekdays:
            PractitionerSchedule.objects.create(
                practitioner=practitioner,
                day_of_week=day,
                start_time=weekday_hours[0],
                end_time=weekday_hours[1],
            )


def unseed_data(apps, schema_editor):
    Service = apps.get_model('bookings', 'Service')
    Practitioner = apps.get_model('bookings', 'Practitioner')
    Practitioner.objects.all().delete()
    Service.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
