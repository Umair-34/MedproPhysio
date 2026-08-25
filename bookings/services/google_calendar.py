"""Optional Google Calendar API integration.

A calendar invite (.ics) is always attached to booking emails, so the clinic
Gmail inbox and Google Calendar can add appointments automatically without any
setup. This module adds the event directly to a shared Google Calendar when the
Google Calendar API is enabled and a service account key is configured.

Enable it with these environment variables:
    GOOGLE_CALENDAR_ENABLED=true
    GOOGLE_CALENDAR_ID=<calendar id or "primary">
    GOOGLE_CALENDAR_CREDENTIALS_FILE=/path/to/service-account.json

Requires the Google client libraries:
    pip install google-api-python-client google-auth
"""

import logging
import os

from django.conf import settings
from django.utils import timezone

from bookings.models import Appointment
from website import content

logger = logging.getLogger(__name__)

_SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def is_enabled() -> bool:
    return bool(
        getattr(settings, 'GOOGLE_CALENDAR_ENABLED', False)
        and getattr(settings, 'GOOGLE_CALENDAR_CREDENTIALS_FILE', '')
    )


def _build_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        logger.warning(
            'Google Calendar sync is enabled but google-api-python-client is not '
            'installed. Run: pip install google-api-python-client google-auth'
        )
        return None

    credentials_file = settings.GOOGLE_CALENDAR_CREDENTIALS_FILE
    if not os.path.exists(credentials_file):
        logger.warning(
            'Google Calendar credentials file not found: %s', credentials_file
        )
        return None

    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=_SCOPES,
    )
    return build('calendar', 'v3', credentials=credentials, cache_discovery=False)


def create_calendar_event(appointment: Appointment) -> str | None:
    """Create a Google Calendar event for the appointment. Returns event id or None."""
    if not is_enabled():
        return None

    service_client = _build_service()
    if service_client is None:
        return None

    tz_name = timezone.get_current_timezone_name()
    customer = appointment.customer
    event_body = {
        'summary': f'{appointment.service.name} - {customer.full_name}',
        'description': (
            f'{appointment.service.name} appointment at {content.SITE_NAME}.\n'
            f'Patient: {customer.full_name}\n'
            f'Phone: {customer.phone}\n'
            f'Email: {customer.email}\n'
            f'Reference: {appointment.confirmation_token}'
            + (f'\nNotes: {appointment.customer_notes}' if appointment.customer_notes else '')
        ),
        'location': content.SITE_ADDRESS,
        'start': {'dateTime': appointment.start_datetime.isoformat(), 'timeZone': tz_name},
        'end': {'dateTime': appointment.end_datetime.isoformat(), 'timeZone': tz_name},
        'attendees': [{'email': customer.email, 'displayName': customer.full_name}],
    }

    try:
        event = service_client.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            body=event_body,
            sendUpdates='all',
        ).execute()
    except Exception:  # noqa: BLE001 - calendar sync must never break booking
        logger.exception(
            'Failed to create Google Calendar event for appointment %s',
            appointment.pk,
        )
        return None

    event_id = event.get('id')
    logger.info(
        'Created Google Calendar event %s for appointment %s', event_id, appointment.pk
    )
    return event_id
