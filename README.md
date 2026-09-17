# MedproPhysio

Django website for **Medpro Physio** in Calgary, Alberta.

## Features

- Online appointment booking with email notifications and calendar invites
- Patient hub with downloadable forms
- Treatments, focus areas, and SEO blog content
- WebP image optimization for faster page loads

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file and configure email, database, and Turnstile keys.

3. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Deploy to DigitalOcean App Platform

The app is configured for production with:

- `STATIC_ROOT` + WhiteNoise for static files
- `gunicorn` as the WSGI server
- PostgreSQL for local development and production (`DATABASE_URL` on DigitalOcean, `POSTGRES_*` locally)
- Environment-based `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`

### Required environment variables

Set these in the DigitalOcean App Platform dashboard:

| Variable | Example |
|----------|---------|
| `SECRET_KEY` | long random string |
| `DEBUG` | `false` |
| `ALLOWED_HOSTS` | `medprophysiotherapy.ca,www.medprophysiotherapy.ca` |
| `CSRF_TRUSTED_ORIGINS` | `https://medprophysiotherapy.ca,https://www.medprophysiotherapy.ca` |
| `SITE_BASE_URL` | `https://medprophysiotherapy.ca` |
| `DATABASE_URL` | auto-injected when you attach a Postgres database |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST_USER` | your Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
| `CLINIC_NOTIFICATION_EMAIL` | `Umair94m@gmail.com` |

### Deploy steps

1. Push to GitHub (`main` branch).
2. Create an App on DigitalOcean, connect the `Umair-34/MedproPhysio` repo.
3. Add a **PostgreSQL** database component (required for production data).
4. Set the environment variables above.
5. Build command (auto-detected): `python manage.py collectstatic --noinput`
6. Run command: `python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2`

See `.do/app.yaml` for a full App Platform spec you can import.

## Environment

Set these in `.env` for local development, including:

- `CLINIC_NOTIFICATION_EMAIL` - clinic inbox(es) for booking and contact alerts (comma-separated, up to several addresses)
- Gmail SMTP settings for sending confirmation emails
- Optional Google Calendar API integration
- `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET`, and `TURNSTILE_HOSTNAMES`
  (production hostnames must be `medprophysiotherapy.ca,www.medprophysiotherapy.ca` only; do not include localhost)
