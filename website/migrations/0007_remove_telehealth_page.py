from django.db import migrations


def remove_telehealth_page(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.filter(section='treatments', slug='telehealth').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_condition_pages'),
    ]

    operations = [
        migrations.RunPython(remove_telehealth_page, migrations.RunPython.noop),
    ]
