from datetime import timedelta
import json

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from bookings.models import Service
from website.spam import issue_form_token


@override_settings(SPAM_MIN_FORM_SECONDS=0, TURNSTILE_SITE_KEY='', TURNSTILE_SECRET='', TURNSTILE_SECRET_KEY='')
class BookingSpamTests(TestCase):
    def setUp(self):
        cache.clear()
        self.service = Service.objects.create(
            name='Physiotherapy',
            slug='physiotherapy-test',
            duration_minutes=45,
            is_active=True,
        )

    def test_booking_without_csrf_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            '/api/bookings/appointments/',
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_honeypot_does_not_create_appointment(self):
        start = timezone.now() + timedelta(days=1)
        response = self.client.post(
            '/api/bookings/appointments/',
            data=json.dumps({
                'service_id': self.service.pk,
                'start_datetime': start.isoformat(),
                'first_name': 'Bot',
                'last_name': 'User',
                'email': 'bot@example.com',
                'phone': '4035550100',
                'form_token': issue_form_token(),
                'company_website': 'https://spam.example',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.service.appointments.count(), 0)
