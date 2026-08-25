"""Seed ContentPage records from legacy Python content modules."""

from website import content
from website import page_content as pc
from website.models import SectionType


def _html_intro(text):
    if not text:
        return ''
    return f'<p>{text}</p>'


def seed_content_pages(apps=None):
    if apps is not None:
        ContentPage = apps.get_model('website', 'ContentPage')
        PageContentSection = apps.get_model('website', 'PageContentSection')
        PageContentBenefit = apps.get_model('website', 'PageContentBenefit')
        PageContentFAQ = apps.get_model('website', 'PageContentFAQ')
    else:
        from website.models import ContentPage, PageContentBenefit, PageContentFAQ, PageContentSection

    if ContentPage.objects.exists():
        return 0

    def create_page(section, item, page_data, sort_order, menu_column=1):
        faqs = page_data.get('faqs', [])
        page = ContentPage.objects.create(
            section=section,
            slug=item['slug'],
            title=item['title'],
            summary=item.get('summary', ''),
            meta_description=page_data.get('meta_description', ''),
            description=_html_intro(page_data.get('intro', '')),
            faq_intro=page_data.get('faq_intro', '') or (pc.DEFAULT_FAQ_INTRO if faqs else ''),
            is_primary=item.get('primary', False),
            menu_column=menu_column,
            sort_order=sort_order,
            is_published=True,
        )
        for index, (heading, body) in enumerate(page_data.get('sections', [])):
            PageContentSection.objects.create(
                page=page,
                heading=heading,
                body=body,
                sort_order=index,
            )
        for index, benefit in enumerate(page_data.get('benefits', [])):
            PageContentBenefit.objects.create(
                page=page,
                text=benefit,
                sort_order=index,
            )
        for index, (question, answer) in enumerate(faqs):
            PageContentFAQ.objects.create(
                page=page,
                question=question,
                answer=answer,
                sort_order=index,
            )
        return page

    created = 0
    for index, item in enumerate(content.FOCUS_AREAS):
        page_data = pc.FOCUS_AREA_PAGES.get(item['slug'], {})
        create_page(SectionType.FOCUS_AREAS, item, page_data, index)
        created += 1

    treatment_pages = pc._build_treatment_pages()
    for index, item in enumerate(content.TREATMENTS_COL1):
        create_page(SectionType.TREATMENTS, item, treatment_pages[item['slug']], index, menu_column=1)
        created += 1
    for index, item in enumerate(content.TREATMENTS_COL2):
        create_page(SectionType.TREATMENTS, item, treatment_pages[item['slug']], index, menu_column=2)
        created += 1

    if apps is None and created:
        from website.page_images import assign_page_images
        assign_page_images(force=True)

    return created
