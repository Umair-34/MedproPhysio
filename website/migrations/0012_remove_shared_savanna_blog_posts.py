from django.db import migrations

DUPLICATE_SAVANNA_SLUGS = [
    'wcb-physiotherapy-claims-calgary',
    'massage-therapy-calgary-benefits',
    'first-physiotherapy-visit-calgary',
    'post-surgery-recovery-physiotherapy-calgary',
    'physiotherapy-chronic-pain-calgary',
    'signs-you-need-physiotherapist-calgary',
    'dry-needling-calgary-benefits',
]


def remove_duplicate_blog_posts(apps, schema_editor):
    BlogPost = apps.get_model('website', 'BlogPost')
    BlogPost.objects.filter(slug__in=DUPLICATE_SAVANNA_SLUGS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_blog_post_and_contact_submission'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_blog_posts, migrations.RunPython.noop),
    ]
