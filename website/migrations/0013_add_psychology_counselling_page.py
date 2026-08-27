from django.db import migrations


def add_psychology_counselling_page(apps, schema_editor):
    from website import content
    from website.models import ContentPage
    from website.page_images import assign_page_images
    from website.treatment_content import all_treatment_content
    from website.treatment_seed import apply_treatment_content

    HistoricalContentPage = apps.get_model('website', 'ContentPage')

    item = next(
        nav_item for nav_item in content.TREATMENTS_COL1
        if nav_item['slug'] == 'psychology-counselling'
    )
    data = all_treatment_content()['psychology-counselling']
    sort_order = next(
        index for index, nav_item in enumerate(content.TREATMENTS_COL1)
        if nav_item['slug'] == 'psychology-counselling'
    )

    historical_page, created = HistoricalContentPage.objects.get_or_create(
        section='treatments',
        slug=item['slug'],
        defaults={
            'title': item['title'],
            'summary': data.get('summary', ''),
            'meta_description': data.get('meta_description', ''),
            'description': data.get('description', ''),
            'typical_sessions': data.get('typical_sessions', ''),
            'first_improvement': data.get('first_improvement', ''),
            'recovery_timeline': data.get('recovery_timeline', ''),
            'benefits_heading': data.get('benefits_heading', 'What this treatment helps with'),
            'faq_intro': data.get('faq_intro', ''),
            'is_primary': item.get('primary', False),
            'menu_column': 1,
            'sort_order': sort_order,
            'is_published': True,
        },
    )

    if not created:
        historical_page.title = item['title']
        historical_page.menu_column = 1
        historical_page.sort_order = sort_order
        historical_page.is_primary = item.get('primary', False)
        historical_page.is_published = True
        historical_page.save()

    page = ContentPage.objects.get(pk=historical_page.pk)
    apply_treatment_content(page, data)
    assign_page_images(pages=[page], force=True)


def remove_psychology_counselling_page(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.filter(section='treatments', slug='psychology-counselling').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_shared_savanna_blog_posts'),
    ]

    operations = [
        migrations.RunPython(add_psychology_counselling_page, remove_psychology_counselling_page),
    ]
