from django.db import migrations


def _html_intro(text):
    if not text:
        return ''
    return f'<p>{text}</p>'


def add_mva_focus_area(apps, schema_editor):
    from website import content
    from website import page_content as pc
    from website.models import ContentPage
    from website.page_images import assign_page_images

    ContentPageModel = apps.get_model('website', 'ContentPage')
    PageContentSection = apps.get_model('website', 'PageContentSection')
    PageContentBenefit = apps.get_model('website', 'PageContentBenefit')
    PageContentFAQ = apps.get_model('website', 'PageContentFAQ')

    item = next(
        nav_item for nav_item in content.FOCUS_AREAS
        if nav_item['slug'] == 'motor-vehicle-accident'
    )
    page_data = pc.FOCUS_AREA_PAGES['motor-vehicle-accident']
    sort_order = next(
        index for index, nav_item in enumerate(content.FOCUS_AREAS)
        if nav_item['slug'] == 'motor-vehicle-accident'
    )
    faqs = page_data.get('faqs', [])

    historical_page, created = ContentPageModel.objects.get_or_create(
        section='focus-areas',
        slug=item['slug'],
        defaults={
            'title': item['title'],
            'summary': item.get('summary', ''),
            'meta_description': page_data.get('meta_description', ''),
            'description': _html_intro(page_data.get('intro', '')),
            'faq_intro': page_data.get('faq_intro', '') or (pc.DEFAULT_FAQ_INTRO if faqs else ''),
            'sort_order': sort_order,
            'is_published': True,
        },
    )

    if not created:
        historical_page.title = item['title']
        historical_page.summary = item.get('summary', '')
        historical_page.meta_description = page_data.get('meta_description', '')
        historical_page.description = _html_intro(page_data.get('intro', ''))
        historical_page.sort_order = sort_order
        historical_page.is_published = True
        historical_page.save()
        PageContentSection.objects.filter(page=historical_page).delete()
        PageContentBenefit.objects.filter(page=historical_page).delete()
        PageContentFAQ.objects.filter(page=historical_page).delete()

    for index, (heading, body) in enumerate(page_data.get('sections', [])):
        PageContentSection.objects.create(
            page=historical_page,
            heading=heading,
            body=body,
            sort_order=index,
        )
    for index, benefit in enumerate(page_data.get('benefits', [])):
        PageContentBenefit.objects.create(
            page=historical_page,
            text=benefit,
            sort_order=index,
        )
    for index, (question, answer) in enumerate(faqs):
        PageContentFAQ.objects.create(
            page=historical_page,
            question=question,
            answer=answer,
            sort_order=index,
        )

    # Reorder existing focus area pages to match content.FOCUS_AREAS
    for index, nav_item in enumerate(content.FOCUS_AREAS):
        ContentPageModel.objects.filter(
            section='focus-areas',
            slug=nav_item['slug'],
        ).update(sort_order=index)

    page = ContentPage.objects.get(pk=historical_page.pk)
    assign_page_images(pages=[page], force=True)


def remove_mva_focus_area(apps, schema_editor):
    ContentPage = apps.get_model('website', 'ContentPage')
    ContentPage.objects.filter(section='focus-areas', slug='motor-vehicle-accident').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_patientdocument'),
    ]

    operations = [
        migrations.RunPython(add_mva_focus_area, remove_mva_focus_area),
    ]
