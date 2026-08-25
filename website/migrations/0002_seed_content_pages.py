from django.db import migrations


def seed_content_pages(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    if ContentPage.objects.exists():
        return
    from website.seed_content import seed_content_pages as run_seed
    run_seed(apps=apps)


def unseed_content_pages(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_content_pages, unseed_content_pages),
    ]
