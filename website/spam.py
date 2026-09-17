"""Lightweight spam guards for public contact and booking forms."""

from __future__ import annotations

import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.core.validators import validate_email

logger = logging.getLogger(__name__)

HONEYPOT_FIELD = 'company_website'
TOKEN_FIELD = 'form_token'
GENERIC_ERROR = (
    'We could not submit that right now. Please try again in a few minutes, '
    'or call the clinic.'
)
_SIGNER = TimestampSigner(salt='medpro-form-guard')
_URL_RE = re.compile(r'https?://', re.IGNORECASE)


class FormGuardError(Exception):
    def __init__(self, message: str, *, silent: bool = False):
        super().__init__(message)
        self.message = message
        self.silent = silent


def issue_form_token() -> str:
    return _SIGNER.sign(str(int(time.time())))


def client_ip(request) -> str:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()[:64]
    return (request.META.get('REMOTE_ADDR') or 'unknown')[:64]


def _get(data, key: str, default: str = '') -> str:
    value = data.get(key, default)
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        value = value[0] if value else default
    return str(value).strip()


def _verify_token(token: str) -> None:
    min_age = int(getattr(settings, 'SPAM_MIN_FORM_SECONDS', 2))
    max_age = int(getattr(settings, 'SPAM_MAX_FORM_SECONDS', 7200))
    try:
        issued = int(_SIGNER.unsign(token, max_age=max_age))
    except (BadSignature, SignatureExpired, TypeError, ValueError) as exc:
        raise FormGuardError(GENERIC_ERROR) from exc
    age = time.time() - issued
    if age < min_age:
        raise FormGuardError(GENERIC_ERROR)


def _rate_limit(key: str, limit: int, window: int) -> None:
    count = cache.get(key, 0)
    if count >= limit:
        raise FormGuardError(GENERIC_ERROR)
    cache.set(key, count + 1, window)


def _turnstile_secret() -> str:
    return (
        getattr(settings, 'TURNSTILE_SECRET', '')
        or getattr(settings, 'TURNSTILE_SECRET_KEY', '')
        or ''
    ).strip()


def _turnstile_hostnames() -> set[str]:
    raw = getattr(settings, 'TURNSTILE_HOSTNAMES', '') or ''
    hosts = {item.strip().split(':')[0] for item in raw.split(',') if item.strip()}
    if getattr(settings, 'DEBUG', False):
        hosts.update({'localhost', '127.0.0.1'})
    return hosts


def _verify_turnstile(request, data, *, expected_action: str) -> None:
    secret = _turnstile_secret()
    sitekey = (getattr(settings, 'TURNSTILE_SITE_KEY', '') or '').strip()
    if not secret:
        if sitekey:
            logger.warning('Turnstile site key is set but TURNSTILE_SECRET is missing')
            raise FormGuardError(GENERIC_ERROR)
        return

    token = _get(data, 'cf-turnstile-response') or _get(data, 'turnstile_token')
    if not isinstance(token, str) or not token or len(token) > 2048:
        raise FormGuardError(GENERIC_ERROR)

    allowed_hosts = _turnstile_hostnames()
    if not allowed_hosts:
        raise FormGuardError(GENERIC_ERROR)

    payload = urllib.parse.urlencode(
        {
            'secret': secret,
            'response': token,
            'remoteip': client_ip(request),
        }
    ).encode()
    req = urllib.request.Request(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        data=payload,
        method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise FormGuardError(GENERIC_ERROR) from exc

    hostname = str(body.get('hostname') or '')
    if (
        not body.get('success')
        or body.get('action') != expected_action
        or hostname not in allowed_hosts
    ):
        logger.info(
            'Turnstile rejected %s (success=%s action=%s hostname=%s)',
            expected_action,
            body.get('success'),
            body.get('action'),
            hostname,
        )
        raise FormGuardError(GENERIC_ERROR)


def _looks_like_spam_text(*parts: str) -> bool:
    combined = ' '.join(part for part in parts if part)
    if len(_URL_RE.findall(combined)) >= 3:
        return True
    if re.search(r'https?://', ' '.join(parts[:2]), re.IGNORECASE):
        return True
    return False


def validate_contact_fields(*, name: str, email: str, message: str, phone: str = '') -> None:
    if len(name) < 2 or len(name) > 120:
        raise FormGuardError('Please enter your name.')
    try:
        validate_email(email)
    except ValidationError as exc:
        raise FormGuardError('Please enter a valid email address.') from exc
    if len(message) < 10 or len(message) > 4000:
        raise FormGuardError('Please enter a short message so we know how to help.')
    digits = re.sub(r'\D', '', phone)
    if phone and len(digits) < 10:
        raise FormGuardError('Please enter a valid phone number.')
    if _looks_like_spam_text(name, email, message):
        raise FormGuardError(GENERIC_ERROR)


def validate_booking_fields(*, first_name: str, last_name: str, email: str, phone: str, notes: str = '') -> None:
    if len(first_name) < 1 or len(first_name) > 80 or len(last_name) > 80:
        raise FormGuardError('Please enter your first and last name.')
    try:
        validate_email(email)
    except ValidationError as exc:
        raise FormGuardError('Please enter a valid email address.') from exc
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 10:
        raise FormGuardError('Please enter a valid phone number.')
    if len(notes) > 2000:
        raise FormGuardError('Please shorten your notes and try again.')
    if _looks_like_spam_text(first_name, last_name, notes):
        raise FormGuardError(GENERIC_ERROR)


def guard_public_form(request, data, *, action: str, limit: int, window: int) -> None:
    """Raise FormGuardError when a public form submission looks automated."""
    if _get(data, HONEYPOT_FIELD):
        logger.info('Blocked %s honeypot from %s', action, client_ip(request))
        raise FormGuardError(GENERIC_ERROR, silent=True)

    _verify_token(_get(data, TOKEN_FIELD))
    _verify_turnstile(request, data, expected_action=action)

    ip = client_ip(request)
    _rate_limit(f'spam:{action}:ip:{ip}', limit, window)
    email = _get(data, 'email').lower()
    if email:
        _rate_limit(f'spam:{action}:email:{email}', limit, window)
