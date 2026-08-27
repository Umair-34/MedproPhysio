import json
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from bookings.models import Appointment, Service
from website.spam import FormGuardError, guard_public_form, validate_booking_fields
from bookings.services.availability import compute_slots
from bookings.services.booking import (
    BookingError,
    PractitionerUnavailableError,
    ServiceUnavailableError,
    SlotUnavailableError,
    cancel_appointment,
    create_appointment,
)


def _parse_date(value: str):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return None


def _parse_datetime(value: str):
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _json_error(message: str, status: int = 400):
    return JsonResponse({'error': message}, status=status)


@require_GET
def service_list(request):
    services = Service.objects.filter(is_active=True)
    data = [
        {
            'id': service.pk,
            'name': service.name,
            'slug': service.slug,
            'description': service.description,
            'duration_minutes': service.duration_minutes,
            'durations': service.allowed_durations(),
            'price': str(service.price) if service.price is not None else None,
        }
        for service in services
    ]
    return JsonResponse({'services': data})


@require_GET
def practitioner_list(request):
    """Practitioners are not used for online booking; kept for API compatibility."""
    return JsonResponse({'practitioners': []})


@require_GET
def available_slots(request):
    service_id = request.GET.get('service_id')
    date_value = request.GET.get('date')
    practitioner_id = request.GET.get('practitioner_id')

    if not service_id or not date_value:
        return _json_error('service_id and date are required.')

    target_date = _parse_date(date_value)
    if target_date is None:
        return _json_error('date must be in YYYY-MM-DD format.')

    service = get_object_or_404(Service, pk=service_id, is_active=True)
    practitioner_pk = int(practitioner_id) if practitioner_id else None
    duration_param = request.GET.get('duration_minutes')
    try:
        duration_minutes = int(duration_param) if duration_param else None
        slots = compute_slots(
            service,
            target_date,
            practitioner_pk,
            duration_minutes=duration_minutes,
        )
    except (TypeError, ValueError):
        return _json_error('duration_minutes must be a number.')
    data = [
        {
            'start_datetime': slot.start_datetime.isoformat(),
            'end_datetime': slot.end_datetime.isoformat(),
            'available_spaces': slot.available_spaces,
        }
        for slot in slots
    ]
    return JsonResponse({'slots': data})


@require_http_methods(['POST'])
def create_booking(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _json_error('Invalid JSON payload.')

    try:
        guard_public_form(
            request,
            payload,
            action='booking',
            limit=settings.SPAM_BOOKING_LIMIT,
            window=settings.SPAM_BOOKING_WINDOW,
        )
    except FormGuardError as exc:
        if exc.silent:
            return _json_error('Unable to complete booking.', status=400)
        return _json_error(exc.message, status=429 if 'few minutes' in exc.message else 400)

    required_fields = ['service_id', 'start_datetime', 'first_name', 'last_name', 'email', 'phone']
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return _json_error(f"Missing required fields: {', '.join(missing)}")

    try:
        validate_booking_fields(
            first_name=str(payload.get('first_name', '')).strip(),
            last_name=str(payload.get('last_name', '')).strip(),
            email=str(payload.get('email', '')).strip(),
            phone=str(payload.get('phone', '')).strip(),
            notes=str(payload.get('customer_notes', '')).strip(),
        )
    except FormGuardError as exc:
        return _json_error(exc.message)

    start_datetime = _parse_datetime(payload['start_datetime'])
    if start_datetime is None:
        return _json_error('start_datetime must be an ISO-8601 datetime string.')

    practitioner_id = payload.get('practitioner_id')
    try:
        appointment = create_appointment(
            service_id=int(payload['service_id']),
            start_datetime=start_datetime,
            practitioner_id=int(practitioner_id) if practitioner_id else None,
            customer_data={
                'first_name': payload['first_name'],
                'last_name': payload['last_name'],
                'email': payload['email'],
                'phone': payload['phone'],
            },
            customer_notes=payload.get('customer_notes', ''),
            duration_minutes=payload.get('duration_minutes'),
        )
    except ServiceUnavailableError as exc:
        return _json_error(str(exc), status=404)
    except PractitionerUnavailableError as exc:
        return _json_error(str(exc), status=400)
    except SlotUnavailableError as exc:
        return _json_error(str(exc), status=409)
    except BookingError as exc:
        return _json_error(str(exc), status=400)
    except (TypeError, ValueError):
        return _json_error('Invalid field values.')

    response_payload = {
        'appointment': {
            'id': appointment.pk,
            'service': appointment.service.name,
            'start_datetime': appointment.start_datetime.isoformat(),
            'end_datetime': appointment.end_datetime.isoformat(),
            'status': appointment.status,
            'duration_minutes': appointment.duration_minutes,
            'confirmation_token': str(appointment.confirmation_token),
        }
    }

    return JsonResponse(response_payload, status=201)


@require_GET
def appointment_detail(request, token):
    appointment = get_object_or_404(Appointment, confirmation_token=token)
    return JsonResponse(
        {
            'appointment': {
                'id': appointment.pk,
                'service': appointment.service.name,
                'practitioner': appointment.practitioner.full_name if appointment.practitioner else None,
                'start_datetime': appointment.start_datetime.isoformat(),
                'end_datetime': appointment.end_datetime.isoformat(),
                'status': appointment.status,
                'customer': {
                    'first_name': appointment.customer.first_name,
                    'last_name': appointment.customer.last_name,
                    'email': appointment.customer.email,
                    'phone': appointment.customer.phone,
                },
                'customer_notes': appointment.customer_notes,
                'confirmation_token': str(appointment.confirmation_token),
            }
        }
    )


@csrf_exempt
@require_http_methods(['POST'])
def cancel_booking(request, token):
    appointment = get_object_or_404(Appointment, confirmation_token=token)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _json_error('Invalid JSON payload.')

    try:
        appointment = cancel_appointment(
            appointment,
            reason=payload.get('reason', ''),
        )
    except BookingError as exc:
        return _json_error(str(exc), status=400)

    return JsonResponse(
        {
            'appointment': {
                'id': appointment.pk,
                'status': appointment.status,
                'cancelled_at': appointment.cancelled_at.isoformat() if appointment.cancelled_at else None,
            }
        }
    )
