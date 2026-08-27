from django.db import migrations


def sync_medpro_blog_posts(apps, schema_editor):
    from website.services.blog import sync_legacy_blog_posts

    sync_legacy_blog_posts()


def unpublish_medpro_blog_posts(apps, schema_editor):
    BlogPost = apps.get_model('website', 'BlogPost')
    BlogPost.objects.filter(
        slug__in=[
            'vestibular-physiotherapy-vertigo-calgary',
            'sciatica-physiotherapy-northwest-calgary',
            'counselling-after-injury-calgary',
            'frozen-shoulder-physiotherapy-calgary',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_add_psychology_counselling_page'),
    ]

    operations = [
        migrations.RunPython(sync_medpro_blog_posts, unpublish_medpro_blog_posts),
    ]
