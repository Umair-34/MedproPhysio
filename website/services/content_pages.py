from website.models import ContentPage, SectionType
from website.page_content import DEFAULT_FAQ_INTRO

PAGE_PREFETCH = (
    'content_sections',
    'benefit_items',
    'faqs',
    'assessment_steps',
    'treatment_methods',
    'recovery_phases',
    'case_studies',
)


def published_pages(section, menu_column=None):
    qs = ContentPage.objects.filter(
        section=section,
        is_published=True,
    ).order_by('sort_order', 'title')
    if menu_column is not None:
        qs = qs.filter(menu_column=menu_column)
    return qs


def nav_items(section, menu_column=None):
    return [page.to_nav_item() for page in published_pages(section, menu_column)]


def get_treatments_col1():
    return nav_items(SectionType.TREATMENTS, menu_column=1)


def get_treatments_col2():
    return nav_items(SectionType.TREATMENTS, menu_column=2)


def get_all_treatments():
    return nav_items(SectionType.TREATMENTS)


def get_content_item(section, slug):
    try:
        page = ContentPage.objects.get(section=section, slug=slug, is_published=True)
    except ContentPage.DoesNotExist:
        return None
    return page.to_nav_item()


def get_page_content(section, slug):
    try:
        page = ContentPage.objects.prefetch_related(*PAGE_PREFETCH).get(
            section=section,
            slug=slug,
            is_published=True,
        )
    except ContentPage.DoesNotExist:
        return None
    return page.to_page_dict(default_faq_intro=DEFAULT_FAQ_INTRO)
