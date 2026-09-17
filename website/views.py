from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from website import blog_content, content
from website.models import ContactSubmission
from website.services import content_pages
from website.services import blog as blog_service
from website.spam import FormGuardError, guard_public_form, issue_form_token, validate_contact_fields
from website.visit import clinic_hours_with_today, clinic_open_status
from bookings.models import Service
from bookings.services.availability import get_bookable_services, get_clinic_weekdays

FOCUS_AREA_REDIRECTS = {
  'sports-recovery': 'sports-performance',
  'workplace-acc-injuries': 'physiotherapy',
  'motor-vehicle-accident': 'physiotherapy',
  'post-surgery-rehab': 'exercise-rehab',
  'balance-vestibular': 'vestibular-therapy',
  'pregnancy-postnatal': 'physiotherapy',
  'chronic-pain': 'myofascial-release',
  'pelvic-health': 'physiotherapy',
  'concussion-recovery': 'concussion-management',
  'acupuncture-wellness': 'acupuncture',
}


@require_GET
def home(request):
  return render(request, 'website/home.html', {
    'home_meta_title': content.HOME_META_TITLE,
    'meta_description': content.HOME_META_DESCRIPTION,
    'home_hero': content.HOME_HERO,
    'home_hero_slides': content.HOME_HERO_SLIDES,
    'home_why_title': content.HOME_WHY_TITLE,
    'home_why_paragraphs': content.HOME_WHY_PARAGRAPHS,
    'home_about_image': content.HOME_ABOUT_IMAGE,
    'home_about_intro': content.HOME_ABOUT_INTRO,
    'home_about_story': content.HOME_ABOUT_STORY,
    'home_about_highlights': content.HOME_ABOUT_HIGHLIGHTS,
    'home_about_stats': content.HOME_ABOUT_STATS,
    'home_counter_value': content.HOME_COUNTER_VALUE,
    'home_counter_label': content.HOME_COUNTER_LABEL,
    'home_first_visit_title': content.HOME_FIRST_VISIT_TITLE,
    'home_first_visit_lead': content.HOME_FIRST_VISIT_LEAD,
    'home_first_visit_intro': content.HOME_FIRST_VISIT_INTRO,
    'home_first_visit_tips': content.HOME_FIRST_VISIT_TIPS,
    'home_first_visit_image': content.HOME_FIRST_VISIT_IMAGE,
    'home_service_promos': content.HOME_SERVICE_PROMOS,
    'home_benefits': content.HOME_BENEFITS,
    'home_about_points': content.HOME_ABOUT_POINTS,
    'home_how_it_works': content.HOME_HOW_IT_WORKS,
    'home_faqs': content.HOME_FAQS,
    'blog_posts': blog_service.get_blog_posts()[:3],
  })


@require_GET
def about(request):
  return render(request, 'website/about.html', {
    'page_title': 'About Us',
    'breadcrumb': 'About Us',
    'page_header_class': 'about-page-header bg-radius-section',
    'meta_description': content.ABOUT_META_DESCRIPTION,
    'about_intro': content.ABOUT_INTRO,
    'about_page_image': content.ABOUT_PAGE_IMAGE,
    'about_page_title': content.ABOUT_PAGE_TITLE,
    'about_page_lead': content.ABOUT_PAGE_LEAD,
    'about_highlights': content.HOME_ABOUT_HIGHLIGHTS,
    'about_stats': content.HOME_ABOUT_STATS,
    'about_counter_value': content.HOME_COUNTER_VALUE,
    'about_counter_label': content.HOME_COUNTER_LABEL,
    'about_mission': content.ABOUT_MISSION,
    'about_vision': content.ABOUT_VISION,
    'about_values': content.ABOUT_VALUES,
    'about_closing': content.ABOUT_CLOSING,
  })


@require_GET
def visit_us(request):
  open_state, open_message = clinic_open_status()
  return render(request, 'website/visit_us.html', {
    'page_title': 'Visit Our Calgary Clinic',
    'breadcrumb': 'Visit Us',
    'page_header_class': 'visit-page-header bg-radius-section',
    'meta_description': (
      f'Visit {content.SITE_NAME} in Calgary, northwest Calgary. Get directions, parking info, '
      'clinic hours, and our Google Business Profile. Physiotherapy and massage near you.'
    ),
    'clinic_hours': clinic_hours_with_today(),
    'clinic_open_state': open_state,
    'clinic_open_message': open_message,
    'visit_parking': content.VISIT_PARKING,
    'visit_transit': content.VISIT_TRANSIT,
    'visit_landmarks': content.VISIT_LANDMARKS,
    'visit_service_areas': content.VISIT_SERVICE_AREAS,
    'visit_faqs': content.VISIT_FAQS,
  })


@require_GET
def contact(request):
  return render(request, 'website/contact.html', {
    'page_title': 'Contact Us',
    'breadcrumb': 'Contact Us',
    'page_header_class': 'contact-page-header bg-radius-section',
    'form_token': issue_form_token(),
  })


@require_POST
def contact_submit(request):
  full_name = request.POST.get('name', '').strip()
  email = request.POST.get('email', '').strip()
  phone = request.POST.get('phone', '').strip()
  message = request.POST.get('message', '').strip()

  try:
    guard_public_form(
      request,
      request.POST,
      action='contact',
      limit=settings.SPAM_CONTACT_LIMIT,
      window=settings.SPAM_CONTACT_WINDOW,
    )
    if not all([full_name, email, message]):
      raise FormGuardError('Please fill in all required fields.')
    validate_contact_fields(name=full_name, email=email, message=message, phone=phone)
  except FormGuardError as exc:
    if exc.silent:
      messages.success(request, 'Thanks. Your message has been sent. We will get back to you soon.')
      return redirect('website:contact')
    messages.error(request, exc.message)
    return redirect('website:contact')

  parts = full_name.split(None, 1)
  first_name = parts[0]
  last_name = parts[1] if len(parts) > 1 else ''

  ContactSubmission.objects.create(
    first_name=first_name,
    last_name=last_name,
    email=email,
    phone=phone,
    message=message,
  )

  clinic_inbox = (getattr(settings, 'CLINIC_NOTIFICATION_EMAIL', '') or content.SITE_EMAIL).strip()
  if clinic_inbox:
    body = (
      f'New contact form submission from the website.\n\n'
      f'Name: {full_name}\n'
      f'Email: {email}\n'
      f'Phone: {phone or "(not provided)"}\n\n'
      f'Message:\n{message}\n'
    )
    try:
      send_mail(
        subject=f'Website contact: {full_name}',
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[clinic_inbox],
        fail_silently=False,
      )
    except Exception:
      # Submission is already saved; do not fail the visitor flow on SMTP issues.
      import logging

      logging.getLogger(__name__).exception('Failed to email contact form submission')

  messages.success(request, 'Thanks. Your message has been sent. We will get back to you soon.')
  return redirect('website:contact')


@ensure_csrf_cookie
@require_GET
def book_appointment(request):
  return render(request, 'website/appointment.html', {
    'page_title': 'Book Appointment',
    'breadcrumb': 'Book Appointment',
    'page_header_class': 'appointment-page-header bg-radius-section',
    'booking_steps': content.BOOKING_STEPS,
    'booking_services': get_bookable_services(),
    'clinic_weekdays': get_clinic_weekdays(),
    'form_token': issue_form_token(),
  })


@require_GET
def faqs(request):
  return render(request, 'website/faqs.html', {
    'page_title': 'FAQs',
    'breadcrumb': 'FAQs',
    'page_hero_lead': content.FAQS_PAGE_LEAD,
    'meta_description': content.FAQS_PAGE_META_DESCRIPTION,
    'faqs_page_categories': content.FAQS_PAGE_CATEGORIES,
    'faqs_page_faqs': content.FAQS_PAGE_FAQS,
  })


@require_GET
def patient_stories(request):
  return render(request, 'website/patient_stories.html', {
    'page_title': 'Patient Stories',
    'breadcrumb': 'Patient Stories',
    'patient_hub_nav': content.PATIENT_HUB,
    'patient_hub_active': 'website:patient-stories',
    'page_hero_lead': 'Google reviews from patients at our northwest Calgary clinic.',
    'meta_description': (
      'Read real Google reviews from patients at Medpro Physiotherapy in northwest Calgary.'
    ),
  })


@require_GET
def blog(request):
  return render(request, 'website/blog.html', {
    'page_title': 'Wellness Blog',
    'breadcrumb': 'Wellness Blog',
    'page_header_class': 'blog-page-header bg-radius-section',
    'meta_title': blog_content.BLOG_META_TITLE,
    'meta_description': blog_content.BLOG_META_DESCRIPTION,
    'page_hero_lead': 'Practical guides on vestibular care, sciatica, frozen shoulder, and counselling after injury at our northwest Calgary clinic.',
    'blog_posts': blog_service.get_blog_posts(),
  })


@require_GET
def blog_detail(request, slug):
  post = blog_service.get_blog_post(slug)
  if post is None:
    raise Http404
  return render(request, 'website/blog_detail.html', {
    'page_title': post['title'],
    'breadcrumb': 'Wellness Blog',
    'post': post,
    'related_posts': blog_service.get_related_posts(slug),
  })


@require_GET
def hub(request, section):
  if section != 'treatments':
    raise Http404
  items = content_pages.get_all_treatments()
  return render(request, 'website/services.html', {
    'page_title': 'Our Services',
    'breadcrumb': 'Our Services',
    'hub_meta_title': content.SERVICES_HUB_META_TITLE,
    'meta_description': content.SERVICES_HUB_META_DESCRIPTION,
    'hub_intro': content.SERVICES_HUB_INTRO,
    'items': items,
    'services_faqs': content.SERVICES_HUB_FAQS,
    'detail_url_name': 'website:service-detail',
    'service_count': len(items),
  })


@require_GET
def legacy_treatment_redirect(request, slug):
  return redirect('website:service-detail', slug=slug, permanent=True)


@require_GET
def focus_area_detail_redirect(request, slug):
  target = FOCUS_AREA_REDIRECTS.get(slug)
  if target:
    return redirect('website:service-detail', slug=target, permanent=True)
  return redirect('website:services', permanent=True)


@require_GET
def detail(request, section, slug):
  if section != 'treatments':
    raise Http404
  item = content_pages.get_content_item(section, slug)
  if item is None:
    raise Http404
  sidebar_items = content_pages.get_all_treatments()
  page = content_pages.get_page_content(section, slug) or {}
  return render(request, 'website/treatment_detail.html', {
    'page_title': f'{item["title"]} Calgary',
    'breadcrumb': item['title'],
    'section': section,
    'section_title': 'Our Services',
    'sidebar_items': sidebar_items,
    'sidebar_url_name': 'website:service-detail',
    'item': item,
    'page': page,
    'is_primary_treatment': item.get('primary', False),
  })


@require_GET
def patient_page(request, slug):
  page = content.PATIENT_PAGES.get(slug)
  if page is None:
    raise Http404

  header_classes = {
    'new-patient': 'patient-guide-page-header bg-radius-section',
    'insurance': 'patient-insurance-page-header bg-radius-section',
  }

  context = {
    'page_title': page['title'],
    'breadcrumb': page['title'],
    'page_header_class': header_classes.get(slug, 'bg-radius-section'),
    'patient_slug': slug,
    'page': page,
    'meta_description': page.get('meta_description', content.SITE_META_DESCRIPTION),
    'patient_hub_nav': content.PATIENT_HUB,
  }

  return render(request, 'website/patient_page.html', context)


def page_not_found(request, exception=None):
  return render(request, '404.html', {
    'page_title': 'Page Not Found',
    'breadcrumb': '404',
    'page_hero_lead': (
      'This page is not available. It may have moved, or the link may be out of date.'
    ),
    'meta_description': (
      'Page not found. Return to Medpro Physiotherapy in northwest Calgary '
      'to book physiotherapy, massage, and wellness care.'
    ),
  }, status=404)


@require_GET
def robots_txt(request):
  sitemap_url = f'{settings.SITE_BASE_URL}/sitemap.xml'
  body = '\n'.join([
    'User-agent: *',
    'Allow: /',
    'Disallow: /admin/',
    'Disallow: /panel/',
    'Disallow: /api/',
    'Disallow: /summernote/',
    '',
    f'Sitemap: {sitemap_url}',
    '',
  ])
  return HttpResponse(body, content_type='text/plain')
