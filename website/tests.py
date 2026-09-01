from django.conf import settings
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


@override_settings(SITE_BASE_URL='https://medprophysiotherapy.ca')
class RobotsAndSitemapTests(TestCase):
    def test_robots_txt_allows_public_pages_and_blocks_private_paths(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/plain'))
        body = response.content.decode()
        self.assertIn('User-agent: *', body)
        self.assertIn('Allow: /', body)
        self.assertIn('Disallow: /admin/', body)
        self.assertIn('Disallow: /panel/', body)
        self.assertIn('Disallow: /api/', body)
        self.assertIn('Disallow: /summernote/', body)
        self.assertIn(f'Sitemap: {settings.SITE_BASE_URL}/sitemap.xml', body)

    def test_sitemap_includes_public_pages_and_excludes_drafts(self):
        from datetime import date

        from website.models import BlogPost, ContentPage, SectionType

        ContentPage.objects.create(
            section=SectionType.TREATMENTS,
            slug='sitemap-test-service',
            title='Sitemap Test Service',
            is_published=True,
        )
        ContentPage.objects.create(
            section=SectionType.TREATMENTS,
            slug='sitemap-test-draft',
            title='Sitemap Test Draft',
            is_published=False,
        )
        BlogPost.objects.create(
            slug='sitemap-test-post',
            title='Sitemap Test Post',
            summary='A published article.',
            published_date=date(2026, 1, 15),
            is_published=True,
        )
        BlogPost.objects.create(
            slug='sitemap-test-unpublished',
            title='Unpublished Post',
            summary='A draft article.',
            published_date=date(2026, 1, 16),
            is_published=False,
        )

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn('xml', response['Content-Type'])
        body = response.content.decode()
        self.assertIn('http://testserver/', body)
        self.assertIn('http://testserver/about/', body)
        self.assertIn('http://testserver/services/', body)
        self.assertIn('http://testserver/services/sitemap-test-service/', body)
        self.assertIn('http://testserver/blog/sitemap-test-post/', body)
        self.assertIn('http://testserver/patient/new-patient/', body)
        self.assertIn('http://testserver/book/', body)
        self.assertNotIn('sitemap-test-draft', body)
        self.assertNotIn('sitemap-test-unpublished', body)
        self.assertNotIn('/admin/', body)
        self.assertNotIn('/panel/', body)


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'],
    SECURE_SSL_REDIRECT=False,
)
class Production404Tests(TestCase):
    def test_unknown_url_shows_branded_404(self):
        response = self.client.get('/this-page-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page Not Found', status_code=404)
        self.assertContains(response, 'Let’s get you back on track', status_code=404)
        self.assertContains(response, 'Back to home', status_code=404)
        self.assertContains(response, 'Book appointment', status_code=404)
        self.assertNotContains(response, 'DEBUG = True', status_code=404)
        self.assertNotContains(response, 'You’re seeing this error because', status_code=404)

    def test_unknown_blog_slug_shows_branded_404(self):
        response = self.client.get('/blog/not-a-real-article/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page Not Found', status_code=404)

    def test_unknown_service_slug_shows_branded_404(self):
        response = self.client.get('/services/not-a-real-service/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page Not Found', status_code=404)
