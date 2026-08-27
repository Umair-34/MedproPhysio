from django.conf import settings
from django.db import migrations, models


def configure_booking_options(apps, schema_editor):
    Service = apps.get_model('bookings', 'Service')
    capacity = max(1, int(getattr(settings, 'BOOKING_SLOT_CAPACITY', 5)))

    massage = Service.objects.filter(slug='massage').first()
    if massage:
        options = [30, int(massage.duration_minutes or 60)]
        massage.duration_options = sorted(set(options))
        massage.save(update_fields=['duration_options'])

    Service.objects.filter(slug='physiotherapy').update(slot_capacity=capacity)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_add_psychology_counselling_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='duration_options',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Extra bookable lengths in minutes, e.g. [30, 60]. The default length is still duration_minutes.',
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='slot_capacity',
            field=models.PositiveIntegerField(
                default=1,
                help_text='How many patients can book the same start time. Use 1 for massage, chiropractic, and kinesiology; higher for physiotherapy.',
            ),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('confirmed', 'Confirmed'),
                    ('cancelled', 'Cancelled'),
                    ('rejected', 'Rejected'),
                    ('completed', 'Completed'),
                    ('no_show', 'No show'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.RunPython(configure_booking_options, noop),
    ]
