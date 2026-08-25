"""Update treatment ContentPage records with patient focused structured content."""

from website import content
from website.models import (
    ContentPage,
    PageAssessmentStep,
    PageCaseStudy,
    PageContentBenefit,
    PageContentFAQ,
    PageContentSection,
    PageRecoveryPhase,
    PageTreatmentMethod,
    SectionType,
)
from website.treatment_content import all_treatment_content


def _clear_related(page):
    page.content_sections.all().delete()
    page.benefit_items.all().delete()
    page.faqs.all().delete()
    page.assessment_steps.all().delete()
    page.treatment_methods.all().delete()
    page.recovery_phases.all().delete()
    page.case_studies.all().delete()


def apply_treatment_content(page, data):
    page.summary = data.get('summary', page.summary)
    page.meta_description = data.get('meta_description', '')
    page.description = data.get('description', '')
    page.typical_sessions = data.get('typical_sessions', '')
    page.first_improvement = data.get('first_improvement', '')
    page.recovery_timeline = data.get('recovery_timeline', '')
    page.benefits_heading = data.get('benefits_heading', 'What this treatment helps with')
    page.faq_intro = data.get('faq_intro', '')
    page.save()

    _clear_related(page)

    for index, (title, body) in enumerate(data.get('assessment_steps', [])):
        PageAssessmentStep.objects.create(
            page=page,
            title=title,
            body=body,
            sort_order=index,
        )

    for index, (title, body) in enumerate(data.get('treatment_methods', [])):
        PageTreatmentMethod.objects.create(
            page=page,
            title=title,
            body=body,
            sort_order=index,
        )

    for index, (phase, timeframe, body) in enumerate(data.get('recovery_phases', [])):
        PageRecoveryPhase.objects.create(
            page=page,
            phase=phase,
            timeframe=timeframe,
            body=body,
            sort_order=index,
        )

    for index, case in enumerate(data.get('case_studies', [])):
        PageCaseStudy.objects.create(
            page=page,
            patient_label=case['patient_label'],
            issue=case['issue'],
            approach=case['approach'],
            outcome=case['outcome'],
            timeline=case['timeline'],
            sort_order=index,
        )

    for index, benefit in enumerate(data.get('benefits', [])):
        PageContentBenefit.objects.create(
            page=page,
            text=benefit,
            sort_order=index,
        )

    for index, (question, answer) in enumerate(data.get('faqs', [])):
        PageContentFAQ.objects.create(
            page=page,
            question=question,
            answer=answer,
            sort_order=index,
        )


def update_all_treatment_pages():
    treatment_data = all_treatment_content()
    updated = 0
    for item in content.all_treatments():
        data = treatment_data.get(item['slug'])
        if not data:
            continue
        try:
            page = ContentPage.objects.get(section=SectionType.TREATMENTS, slug=item['slug'])
        except ContentPage.DoesNotExist:
            continue
        apply_treatment_content(page, data)
        updated += 1
    return updated
