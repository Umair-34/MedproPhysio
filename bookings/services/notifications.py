"""Email notifications and calendar invites for appointment bookings."""

import logging
from datetime import timezone as dt_timezone
from email.mime.image import MIMEImage
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from bookings.models import Appointment
from website import content

logger = logging.getLogger(__name__)

DATE_FORMAT = '%A, %B %-d, %Y'
TIME_FORMAT = '%-I:%M %p'
ICS_TIMESTAMP_FORMAT = '%Y%m%dT%H%M%SZ'
EMAIL_LOGO_CID = 'clinic-logo'
EMAIL_LOGO_CANDIDATES = (
    'images/medpro-logo.png',
    'images/medpro-logo-light.png',
    'images/medpro-logo-icon.png',
)


def _ics_datetime(value) -> str:
    return value.astimezone(dt_timezone.utc).strftime(ICS_TIMESTAMP_FORMAT)


def _ics_escape(text: str) -> str:
    return (
        str(text)
        .replace('\\', '\\\\')
        .replace(';', '\\;')
        .replace(',', '\\,')
        .replace('\n', '\\n')
    )


def build_ics(appointment: Appointment, *, method: str = 'REQUEST', cancelled: bool = False) -> str:
    """Return an iCalendar (.ics) invite for the appointment."""
    service = appointment.service
    customer = appointment.customer
    summary = f'{service.name} - {content.SITE_NAME}'
    status = 'CANCELLED' if cancelled else 'CONFIRMED'
    sequence = 1 if cancelled else 0

    description = (
        f'{service.name} appointment at {content.SITE_NAME}.\\n'
        f'Reference: {appointment.confirmation_token}'
    )
    if appointment.customer_notes:
        description += f'\\nNotes: {_ics_escape(appointment.customer_notes)}'

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Medpro Physiotherapy//Booking//EN',
        'CALSCALE:GREGORIAN',
        f'METHOD:{method}',
        'BEGIN:VEVENT',
        f'UID:{appointment.confirmation_token}@medprophysiotherapy.ca',
        f'DTSTAMP:{_ics_datetime(timezone.now())}',
        f'DTSTART:{_ics_datetime(appointment.start_datetime)}',
        f'DTEND:{_ics_datetime(appointment.end_datetime)}',
        f'SUMMARY:{_ics_escape(summary)}',
        f'DESCRIPTION:{description}',
        f'LOCATION:{_ics_escape(content.SITE_ADDRESS)}',
        f'STATUS:{status}',
        f'SEQUENCE:{sequence}',
        f'ORGANIZER;CN={_ics_escape(content.SITE_NAME)}:mailto:{_clinic_email()}',
        (
            f'ATTENDEE;CN={_ics_escape(customer.full_name)};ROLE=REQ-PARTICIPANT;'
            f'RSVP=TRUE:mailto:{customer.email}'
        ),
        'END:VEVENT',
        'END:VCALENDAR',
    ]
    return '\r\n'.join(lines)


def _split_emails(value) -> list[str]:
    if isinstance(value, (list, tuple)):
        parts = value
    else:
        parts = str(value or '').replace(';', ',').split(',')
    emails = []
    seen = set()
    for part in parts:
        email = str(part).strip()
        if not email:
            continue
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        emails.append(email)
    return emails


def clinic_notification_emails() -> list[str]:
    configured = getattr(settings, 'CLINIC_NOTIFICATION_EMAILS', None)
    emails = _split_emails(configured) if configured else []
    if emails:
        return emails
    raw = getattr(settings, 'CLINIC_NOTIFICATION_EMAIL', '') or content.SITE_EMAIL
    return _split_emails(raw)


def _clinic_email() -> str:
    emails = clinic_notification_emails()
    return emails[0] if emails else content.SITE_EMAIL.strip()


def _recipient_list(value) -> list[str]:
    emails = _split_emails(value)
    return emails or clinic_notification_emails()


def _find_email_logo() -> Path | None:
    for candidate in EMAIL_LOGO_CANDIDATES:
        found = finders.find(candidate)
        if found:
            return Path(found)
    return None


def email_logo_url() -> str:
    """Public URL for the clinic logo (CDN in production, site origin otherwise)."""
    url = staticfiles_storage.url(EMAIL_LOGO_CANDIDATES[0])
    if url.startswith(('http://', 'https://')):
        return url
    base = settings.SITE_BASE_URL.rstrip('/')
    return f'{base}{url}' if url.startswith('/') else f'{base}/{url}'


def attach_email_logo(message: EmailMultiAlternatives) -> bool:
    """Attach the clinic logo inline so email clients do not fetch a remote URL."""
    path = _find_email_logo()
    if path is None or not path.is_file():
        return False
    subtype = 'png' if path.suffix.lower() == '.png' else path.suffix.lstrip('.').lower() or 'png'
    image = MIMEImage(path.read_bytes(), _subtype=subtype)
    image.add_header('Content-ID', f'<{EMAIL_LOGO_CID}>')
    image.add_header('Content-Disposition', 'inline', filename=path.name)
    message.mixed_subtype = 'related'
    message.attach(image)
    return True


def _logo_url_for_context() -> str:
    if _find_email_logo() is not None:
        return f'cid:{EMAIL_LOGO_CID}'
    return email_logo_url()


def _base_context(appointment: Appointment) -> dict:
    customer = appointment.customer
    service = appointment.service
    start_local = timezone.localtime(appointment.start_datetime)
    site_base = settings.SITE_BASE_URL.rstrip('/')
    return {
        'clinic_name': content.SITE_NAME,
        'clinic_address': content.SITE_ADDRESS,
        'clinic_address_short': content.SITE_ADDRESS_SHORT,
        'clinic_phone': content.SITE_PHONE,
        'clinic_phone_link': content.SITE_PHONE_LINK.replace('tel:', ''),
        'clinic_email': content.SITE_EMAIL,
        'clinic_hours': content.WORKING_HOURS,
        'directions_url': content.SITE_GOOGLE_DIRECTIONS_URL,
        'book_url': f'{site_base}/book/',
        'site_base_url': site_base,
        'logo_url': _logo_url_for_context(),
        'service_name': service.name,
        'duration_minutes': appointment.duration_minutes,
        'appointment_date': start_local.strftime(DATE_FORMAT),
        'appointment_time': start_local.strftime(TIME_FORMAT),
        'practitioner_name': appointment.practitioner.full_name if appointment.practitioner else '',
        'status_label': appointment.get_status_display(),
        'customer_name': customer.full_name,
        'customer_first_name': customer.first_name,
        'customer_email': customer.email,
        'customer_phone': customer.phone,
        'customer_notes': appointment.customer_notes,
        'confirmation_token': str(appointment.confirmation_token),
        'cancellation_reason': appointment.cancellation_reason,
    }


def _send(
    *,
    subject: str,
    to_email: str | list[str],
    html_template: str,
    text_template: str,
    context: dict,
    ics_content: str | None,
    ics_method: str,
    reply_to: list[str] | None = None,
) -> None:
    html_body = render_to_string(html_template, context)
    text_body = render_to_string(text_template, context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=_recipient_list(to_email),
        reply_to=reply_to,
    )
    message.attach_alternative(html_body, 'text/html')
    attach_email_logo(message)

    if ics_content:
        # Attach as UTF-8 bytes so non-ASCII notes/addresses do not break SMTP.
        message.attach(
            'invite.ics',
            ics_content.encode('utf-8'),
            f'text/calendar; method={ics_method}; charset=UTF-8',
        )

    message.send(fail_silently=False)


def send_booking_request(appointment: Appointment) -> None:
    """Email the clinic that a new online request needs approve or reject."""
    try:
        base = _base_context(appointment)
        when = f"{base['appointment_date']} at {base['appointment_time']}"
        _send(
            subject=f"New booking request: {base['service_name']} - {base['customer_name']} ({when})",
            to_email=clinic_notification_emails(),
            html_template='emails/booking_request.html',
            text_template='emails/booking_request.txt',
            context={**base, 'audience': 'clinic', 'show_patient': True},
            ics_content=None,
            ics_method='REQUEST',
            reply_to=[appointment.customer.email],
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            'Failed to send booking request email for appointment %s',
            appointment.pk,
        )


def send_booking_confirmation(appointment: Appointment, *, notify_clinic: bool = False) -> None:
    """Email the client that a booking is confirmed. Optionally copy the clinic."""
    try:
        ics_content = build_ics(appointment, method='REQUEST')
        base = _base_context(appointment)
        when = f"{base['appointment_date']} at {base['appointment_time']}"

        _send(
            subject=f"Your appointment is confirmed - {base['appointment_date']}",
            to_email=appointment.customer.email,
            html_template='emails/booking_confirmation.html',
            text_template='emails/booking_confirmation.txt',
            context={**base, 'audience': 'client', 'show_patient': False},
            ics_content=ics_content,
            ics_method='REQUEST',
            reply_to=[_clinic_email()],
        )

        if notify_clinic:
            _send(
                subject=f"Confirmed booking: {base['service_name']} - {base['customer_name']} ({when})",
                to_email=clinic_notification_emails(),
                html_template='emails/booking_confirmation.html',
                text_template='emails/booking_confirmation.txt',
                context={**base, 'audience': 'clinic', 'show_patient': True},
                ics_content=ics_content,
                ics_method='REQUEST',
                reply_to=[appointment.customer.email],
            )
    except Exception:  # noqa: BLE001 - notifications must never break booking
        logger.exception(
            'Failed to send booking confirmation emails for appointment %s',
            appointment.pk,
        )


def send_booking_rejection(appointment: Appointment) -> None:
    """Email the client that their request was not approved."""
    try:
        base = _base_context(appointment)
        _send(
            subject=f"Your appointment request on {base['appointment_date']} was not approved",
            to_email=appointment.customer.email,
            html_template='emails/booking_rejection.html',
            text_template='emails/booking_rejection.txt',
            context={**base, 'audience': 'client', 'show_patient': False},
            ics_content=None,
            ics_method='CANCEL',
            reply_to=[_clinic_email()],
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            'Failed to send booking rejection email for appointment %s',
            appointment.pk,
        )


def send_booking_cancellation(appointment: Appointment) -> None:
    """Email the client and the clinic that a booking was cancelled."""
    try:
        ics_content = build_ics(appointment, method='CANCEL', cancelled=True)
        base = _base_context(appointment)

        _send(
            subject=f"Your appointment on {base['appointment_date']} is cancelled",
            to_email=appointment.customer.email,
            html_template='emails/booking_cancellation.html',
            text_template='emails/booking_cancellation.txt',
            context={**base, 'audience': 'client', 'show_patient': False},
            ics_content=ics_content,
            ics_method='CANCEL',
            reply_to=[_clinic_email()],
        )

        _send(
            subject=f"Cancelled: {base['service_name']} - {base['customer_name']} ({base['appointment_date']})",
            to_email=clinic_notification_emails(),
            html_template='emails/booking_cancellation.html',
            text_template='emails/booking_cancellation.txt',
            context={**base, 'audience': 'clinic', 'show_patient': True},
            ics_content=ics_content,
            ics_method='CANCEL',
            reply_to=[appointment.customer.email],
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            'Failed to send booking cancellation emails for appointment %s',
            appointment.pk,
        )


def send_booking_update(
    appointment: Appointment,
    *,
    previous: dict | None = None,
    message: str = '',
) -> None:
    """Email the customer (and clinic) that an existing booking changed."""
    try:
        ics_content = build_ics(appointment, method='REQUEST')
        base = _base_context(appointment)
        previous = previous or {}
        context = {
            **base,
            'audience': 'client',
            'show_patient': False,
            'update_message': message.strip(),
            'previous_service_name': previous.get('service_name', ''),
            'previous_appointment_date': previous.get('appointment_date', ''),
            'previous_appointment_time': previous.get('appointment_time', ''),
        }
        when = f"{base['appointment_date']} at {base['appointment_time']}"

        _send(
            subject=f"Your appointment has been updated - {base['appointment_date']}",
            to_email=appointment.customer.email,
            html_template='emails/booking_update.html',
            text_template='emails/booking_update.txt',
            context=context,
            ics_content=ics_content,
            ics_method='REQUEST',
            reply_to=[_clinic_email()],
        )

        _send(
            subject=f"Updated booking: {base['service_name']} - {base['customer_name']} ({when})",
            to_email=clinic_notification_emails(),
            html_template='emails/booking_update.html',
            text_template='emails/booking_update.txt',
            context={**context, 'audience': 'clinic', 'show_patient': True},
            ics_content=ics_content,
            ics_method='REQUEST',
            reply_to=[appointment.customer.email],
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            'Failed to send booking update emails for appointment %s',
            appointment.pk,
        )
