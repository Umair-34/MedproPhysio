from django.db import migrations


def delete_condition_pages(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.filter(section='conditions').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_treatment_structured_content'),
    ]

    operations = [
        migrations.RunPython(delete_condition_pages, migrations.RunPython.noop),
    ]
