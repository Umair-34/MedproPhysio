from datetime import datetime, time, timedelta
import json

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from unittest.mock import patch

from bookings.models import Appointment, Customer, Service
from bookings.services.availability import AvailableSlot
from bookings.services.booking import (
    DEFAULT_REJECT_MESSAGE,
    approve_appointment,
    create_appointment,
    reject_appointment,
)
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


class AppointmentReviewTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Physiotherapy',
            slug='physiotherapy-review',
            duration_minutes=45,
            is_active=True,
        )
        self.customer = Customer.objects.create(
            first_name='Jane',
            last_name='Patient',
            email='jane@example.com',
            phone='4035550100',
        )
        start = timezone.now() + timedelta(days=2)
        self.appointment = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_datetime=start,
            end_datetime=start + timedelta(minutes=45),
            status=Appointment.Status.PENDING,
        )

    @patch('bookings.services.booking.send_booking_request')
    @patch('bookings.services.booking.send_booking_confirmation')
    @patch('bookings.services.booking.is_slot_available')
    def test_create_appointment_notifies_clinic_only(
        self, mock_slot, mock_confirm, mock_request
    ):
        start = timezone.now() + timedelta(days=1)
        mock_slot.return_value = AvailableSlot(
            start_datetime=start,
            end_datetime=start + timedelta(minutes=45),
            available_spaces=5,
        )
        with self.captureOnCommitCallbacks(execute=True):
            appointment = create_appointment(
                service_id=self.service.pk,
                start_datetime=start,
                customer_data={
                    'first_name': 'Sam',
                    'last_name': 'Lee',
                    'email': 'sam@example.com',
                    'phone': '4035550199',
                },
            )
        self.assertEqual(appointment.status, Appointment.Status.PENDING)
        mock_request.assert_called_once()
        mock_confirm.assert_not_called()

    @patch('bookings.services.booking.send_booking_confirmation')
    @patch('bookings.services.booking.create_calendar_event')
    def test_approve_confirms_and_notifies_client(self, mock_calendar, mock_email):
        with self.captureOnCommitCallbacks(execute=True):
            approved = approve_appointment(self.appointment)
        self.assertEqual(approved.status, Appointment.Status.CONFIRMED)
        mock_email.assert_called_once()
        mock_calendar.assert_called_once()

    @patch('bookings.services.booking.send_booking_rejection')
    def test_reject_uses_default_message(self, mock_email):
        with self.captureOnCommitCallbacks(execute=True):
            rejected = reject_appointment(self.appointment, reason='')
        self.assertEqual(rejected.status, Appointment.Status.REJECTED)
        self.assertEqual(rejected.cancellation_reason, DEFAULT_REJECT_MESSAGE)
        mock_email.assert_called_once()

    @patch('bookings.services.booking.send_booking_rejection')
    def test_reject_keeps_staff_message(self, mock_email):
        with self.captureOnCommitCallbacks(execute=True):
            rejected = reject_appointment(
                self.appointment,
                reason='Please choose Saturday morning instead.',
            )
        self.assertEqual(
            rejected.cancellation_reason,
            'Please choose Saturday morning instead.',
        )
        mock_email.assert_called_once()

    def test_panel_approve_and_reject_endpoints(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        User.objects.create_user(username='staff', password='pass-word', is_staff=True)
        client = Client()
        client.login(username='staff', password='pass-word')

        with patch('bookings.services.booking.send_booking_confirmation'), patch(
            'bookings.services.booking.create_calendar_event'
        ):
            response = client.post(f'/panel/api/appointments/{self.appointment.pk}/approve/')
        self.assertEqual(response.status_code, 200)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, Appointment.Status.CONFIRMED)

        later = timezone.now() + timedelta(days=3)
        other = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_datetime=later,
            end_datetime=later + timedelta(minutes=45),
            status=Appointment.Status.PENDING,
        )
        with patch('bookings.services.booking.send_booking_rejection'):
            response = client.post(
                f'/panel/api/appointments/{other.pk}/reject/',
                data=json.dumps({'reason': 'This slot is already booked. Kindly book another slot.'}),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        other.refresh_from_db()
        self.assertEqual(other.status, Appointment.Status.REJECTED)

    def test_calendar_title_uses_time_service_and_first_name(self):
        from django.contrib.auth import get_user_model
        from panel.views import _calendar_event_title

        title = _calendar_event_title(self.appointment)
        start_local = timezone.localtime(self.appointment.start_datetime)
        if start_local.minute:
            time_label = start_local.strftime('%-I:%M %p')
        else:
            time_label = start_local.strftime('%-I %p')
        self.assertEqual(title, f'({time_label} Physiotherapy) Jane')

        User = get_user_model()
        User.objects.create_user(username='staff', password='pass-word', is_staff=True)
        client = Client()
        client.login(username='staff', password='pass-word')
        response = client.get('/panel/api/appointments/')
        self.assertEqual(response.status_code, 200)
        events = response.json()['events']
        self.assertEqual(events[0]['title'], title)
        self.assertEqual(events[0]['extendedProps']['patient_name'], 'Jane Patient')


class BookableServiceTests(TestCase):
    def test_massage_is_one_service_with_two_lengths(self):
        service = Service.objects.get(slug='massage')
        self.assertEqual(service.name, 'Massage')
        self.assertEqual(service.allowed_durations(), [30, 60])
        self.assertFalse(Service.objects.filter(slug='massage-30').exists())

    def test_massage_rejects_an_invalid_length(self):
        service = Service.objects.get(slug='massage')
        with self.assertRaises(ValueError):
            service.resolve_duration(90)

    def test_create_appointment_keeps_requested_massage_length(self):
        service = Service.objects.get(slug='massage')
        start = timezone.now() + timedelta(days=1)
        slot_end = start + timedelta(minutes=30)
        with patch('bookings.services.booking.send_booking_request'), patch(
            'bookings.services.booking.is_slot_available',
            return_value=AvailableSlot(
                start_datetime=start,
                end_datetime=slot_end,
                available_spaces=5,
            ),
        ):
            with self.captureOnCommitCallbacks(execute=True):
                appointment = create_appointment(
                    service_id=service.pk,
                    start_datetime=start,
                    duration_minutes=30,
                    customer_data={
                        'first_name': 'Sam',
                        'last_name': 'Lee',
                        'email': 'sam@example.com',
                        'phone': '4035550199',
                    },
                )
        self.assertEqual(appointment.service_id, service.pk)
        self.assertEqual(appointment.duration_minutes, 30)


class SlotCapacityTests(TestCase):
    def setUp(self):
        self.massage = Service.objects.create(
            name='Massage',
            slug='massage-capacity',
            duration_minutes=60,
            slot_capacity=1,
            is_active=True,
        )
        self.physio = Service.objects.create(
            name='Physiotherapy',
            slug='physio-capacity',
            duration_minutes=45,
            slot_capacity=5,
            is_active=True,
        )
        self.chiro = Service.objects.create(
            name='Chiropractic',
            slug='chiro-capacity',
            duration_minutes=30,
            slot_capacity=1,
            is_active=True,
        )

    def _next_weekday_afternoon(self):
        current = timezone.localtime(timezone.now()) + timedelta(days=1)
        current = current.replace(hour=13, minute=0, second=0, microsecond=0)
        while current.weekday() >= 5:
            current += timedelta(days=1)
        return current

    def _book(self, service, start, first_name='Sam'):
        with patch('bookings.services.booking.send_booking_request'):
            with self.captureOnCommitCallbacks(execute=True):
                return create_appointment(
                    service_id=service.pk,
                    start_datetime=start,
                    customer_data={
                        'first_name': first_name,
                        'last_name': 'Lee',
                        'email': f'{first_name.lower()}@example.com',
                        'phone': '4035550199',
                    },
                )

    def test_massage_and_chiro_allow_one_booking_per_slot(self):
        from bookings.services.booking import SlotUnavailableError

        start = self._next_weekday_afternoon()
        self._book(self.massage, start, 'One')
        with self.assertRaises(SlotUnavailableError):
            self._book(self.massage, start, 'Two')

        self._book(self.chiro, start, 'Chiro')
        with self.assertRaises(SlotUnavailableError):
            self._book(self.chiro, start, 'ChiroTwo')

    def test_physiotherapy_allows_multiple_bookings_on_the_same_slot(self):
        start = self._next_weekday_afternoon()
        first = self._book(self.physio, start, 'One')
        second = self._book(self.physio, start, 'Two')
        self.assertEqual(first.start_datetime, second.start_datetime)
        self.assertEqual(
            Appointment.objects.filter(service=self.physio, start_datetime=start).count(),
            2,
        )

    def test_massage_slot_disappears_after_it_is_taken(self):
        from bookings.services.availability import compute_slots

        start = self._next_weekday_afternoon()
        self._book(self.massage, start, 'One')
        remaining = [
            slot.start_datetime
            for slot in compute_slots(self.massage, start.date(), duration_minutes=60)
        ]
        self.assertNotIn(start, remaining)

    def test_rejected_slot_stays_hidden_from_other_clients(self):
        from bookings.services.availability import compute_slots
        from bookings.services.booking import SlotUnavailableError, reject_appointment

        start = self._next_weekday_afternoon()
        appointment = self._book(self.massage, start, 'One')
        with patch('bookings.services.booking.send_booking_rejection'):
            with self.captureOnCommitCallbacks(execute=True):
                reject_appointment(appointment)

        remaining = [
            slot.start_datetime
            for slot in compute_slots(self.massage, start.date(), duration_minutes=60)
        ]
        self.assertNotIn(start, remaining)
        with self.assertRaises(SlotUnavailableError):
            self._book(self.massage, start, 'Two')

    def test_rejected_physio_slot_stays_hidden(self):
        from bookings.services.availability import compute_slots
        from bookings.services.booking import reject_appointment

        start = self._next_weekday_afternoon()
        appointment = self._book(self.physio, start, 'One')
        with patch('bookings.services.booking.send_booking_rejection'):
            with self.captureOnCommitCallbacks(execute=True):
                reject_appointment(appointment)

        remaining = [
            slot.start_datetime
            for slot in compute_slots(self.physio, start.date(), duration_minutes=45)
        ]
        self.assertNotIn(start, remaining)

    def test_cancelled_appointment_frees_the_slot(self):
        from bookings.services.availability import compute_slots
        from bookings.services.booking import cancel_appointment

        start = self._next_weekday_afternoon()
        appointment = self._book(self.massage, start, 'One')
        with patch('bookings.services.booking.send_booking_rejection'):
            with self.captureOnCommitCallbacks(execute=True):
                cancel_appointment(appointment)

        remaining = [
            slot.start_datetime
            for slot in compute_slots(self.massage, start.date(), duration_minutes=60)
        ]
        self.assertIn(start, remaining)


class DashboardTodayTests(TestCase):
    def test_dashboard_lists_every_appointment_for_today(self):
        from django.contrib.auth import get_user_model

        service = Service.objects.create(
            name='Massage',
            slug='massage-today-list',
            duration_minutes=30,
            slot_capacity=1,
            is_active=True,
        )
        today = timezone.localdate()
        tz = timezone.get_current_timezone()
        User = get_user_model()
        User.objects.create_user(username='staff', password='pass-word', is_staff=True)
        client = Client()
        client.login(username='staff', password='pass-word')

        for index in range(10):
            customer = Customer.objects.create(
                first_name=f'Pat{index}',
                last_name='Client',
                email=f'pat{index}@example.com',
                phone='4035550100',
            )
            start = timezone.make_aware(
                datetime.combine(today, time(9, 0)) + timedelta(minutes=index * 5),
                tz,
            )
            Appointment.objects.create(
                customer=customer,
                service=service,
                start_datetime=start,
                end_datetime=start + timedelta(minutes=30),
                status=Appointment.Status.CONFIRMED,
            )

        tomorrow_customer = Customer.objects.create(
            first_name='Later',
            last_name='Client',
            email='later@example.com',
            phone='4035550100',
        )
        tomorrow = timezone.make_aware(datetime.combine(today + timedelta(days=1), time(10, 0)), tz)
        Appointment.objects.create(
            customer=tomorrow_customer,
            service=service,
            start_datetime=tomorrow,
            end_datetime=tomorrow + timedelta(minutes=30),
            status=Appointment.Status.CONFIRMED,
        )

        response = client.get('/panel/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today's appointments")
        self.assertContains(response, '10 bookings')
        self.assertContains(response, 'Pat9 Client')
        self.assertNotContains(response, 'Later Client')
