from django.db import migrations


def remove_tmj_jaw_care_page(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.filter(section='focus-areas', slug='tmj-jaw-care').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_contentpage_image'),
    ]

    operations = [
        migrations.RunPython(remove_tmj_jaw_care_page, migrations.RunPython.noop),
    ]
