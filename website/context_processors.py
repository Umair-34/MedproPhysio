from django.conf import settings

from website import content
from website.services import content_pages
from website.visit import clinic_hours_with_today, clinic_open_status


def site(request):
  open_state, open_message = clinic_open_status()
  return {
    'use_r2': getattr(settings, 'USE_R2', False),
    'site_name': content.SITE_NAME,
    'site_tagline': content.SITE_TAGLINE,
    'site_meta_description': content.SITE_META_DESCRIPTION,
    'site_phone': content.SITE_PHONE,
    'site_phone_link': content.SITE_PHONE_LINK,
    'site_cta': content.SITE_CTA,
    'site_email': content.SITE_EMAIL,
    'site_address': content.SITE_ADDRESS,
    'site_address_short': content.SITE_ADDRESS_SHORT,
    'site_street_address': content.SITE_STREET_ADDRESS,
    'site_postal_code': content.SITE_POSTAL_CODE,
    'site_city': content.SITE_CITY,
    'site_region': content.SITE_REGION,
    'site_country': content.SITE_COUNTRY,
    'site_latitude': content.SITE_LATITUDE,
    'site_longitude': content.SITE_LONGITUDE,
    'site_map_url': content.SITE_MAP_URL,
    'site_map_embed_url': content.SITE_MAP_EMBED_URL,
    'site_google_business_url': content.SITE_GOOGLE_BUSINESS_URL,
    'site_google_directions_url': content.SITE_GOOGLE_DIRECTIONS_URL,
    'site_google_review_url': content.google_review_url(),
    'site_google_place_id': content.SITE_GOOGLE_PLACE_ID,
    'clinic_open_state': open_state,
    'clinic_open_message': open_message,
    'clinic_hours': clinic_hours_with_today(),
    'opening_hours_schema': content.OPENING_HOURS_SCHEMA,
    'working_hours': content.WORKING_HOURS,
    'treatments_col1': content_pages.get_treatments_col1(),
    'treatments_col2': content_pages.get_treatments_col2(),
    'all_services': content_pages.get_all_treatments(),
    'patient_hub': content.PATIENT_HUB,
    'site_testimonials': content.SITE_TESTIMONIALS,
    'about_intro': content.ABOUT_INTRO,
    'about_mission': content.ABOUT_MISSION,
    'about_vision': content.ABOUT_VISION,
    'about_values': content.ABOUT_VALUES,
    'about_closing': content.ABOUT_CLOSING,
    'turnstile_site_key': getattr(settings, 'TURNSTILE_SITE_KEY', ''),
  }
