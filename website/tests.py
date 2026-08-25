from django.core.cache import cache
from django.test import TestCase, override_settings
from django.core import mail
from unittest.mock import patch, MagicMock
import json

from website.models import ContactSubmission
from website.spam import issue_form_token


def _mock_siteverify(success=True, action='contact', hostname='127.0.0.1'):
    body = json.dumps({
        'success': success,
        'action': action,
        'hostname': hostname,
    }).encode()
    response = MagicMock()
    response.read.return_value = body
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


@override_settings(
    SPAM_MIN_FORM_SECONDS=0,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TURNSTILE_SITE_KEY='',
    TURNSTILE_SECRET='',
    TURNSTILE_SECRET_KEY='',
)
class ContactSpamTests(TestCase):
    def setUp(self):
        cache.clear()
        mail.outbox.clear()

    def _payload(self, **overrides):
        data = {
            'name': 'Jane Patient',
            'email': 'jane@example.com',
            'phone': '4035550100',
            'message': 'I would like to ask about physiotherapy availability.',
            'form_token': issue_form_token(),
            'company_website': '',
        }
        data.update(overrides)
        return data

    def test_valid_message_is_saved(self):
        response = self.client.post('/api/contact/', self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.objects.count(), 1)

    def test_honeypot_is_silently_dropped(self):
        response = self.client.post(
            '/api/contact/',
            self._payload(company_website='https://spam.example'),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_token_is_rejected(self):
        self.client.post('/api/contact/', self._payload(form_token=''))
        self.assertEqual(ContactSubmission.objects.count(), 0)

    def test_rate_limit_blocks_repeat_submissions(self):
        for _ in range(3):
            self.client.post('/api/contact/', self._payload())
        self.assertEqual(ContactSubmission.objects.count(), 3)
        self.client.post('/api/contact/', self._payload())
        self.assertEqual(ContactSubmission.objects.count(), 3)


@override_settings(
    SPAM_MIN_FORM_SECONDS=0,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TURNSTILE_SITE_KEY='0x4AAAAAAEXc4MbXldOrAHGn',
    TURNSTILE_SECRET='test-secret',
    TURNSTILE_SECRET_KEY='test-secret',
    TURNSTILE_HOSTNAMES='127.0.0.1',
    DEBUG=True,
)
class ContactTurnstileTests(TestCase):
    def setUp(self):
        cache.clear()
        mail.outbox.clear()

    def _payload(self, **overrides):
        data = {
            'name': 'Jane Patient',
            'email': 'jane@example.com',
            'phone': '4035550100',
            'message': 'I would like to ask about physiotherapy availability.',
            'form_token': issue_form_token(),
            'company_website': '',
            'cf-turnstile-response': 'fresh-token',
        }
        data.update(overrides)
        return data

    def test_missing_token_is_rejected(self):
        self.client.post('/api/contact/', self._payload(**{'cf-turnstile-response': ''}))
        self.assertEqual(ContactSubmission.objects.count(), 0)

    @patch('website.spam.urllib.request.urlopen')
    def test_valid_token_is_accepted(self, urlopen):
        urlopen.return_value = _mock_siteverify()
        response = self.client.post('/api/contact/', self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        urlopen.assert_called_once()

    @patch('website.spam.urllib.request.urlopen')
    def test_wrong_action_is_rejected(self, urlopen):
        urlopen.return_value = _mock_siteverify(action='booking')
        self.client.post('/api/contact/', self._payload())
        self.assertEqual(ContactSubmission.objects.count(), 0)
