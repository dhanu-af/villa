"""
Django settings for the Cannelle Hill Cabanas website.

Uses SQLite by default for local development. Set the DATABASE_URL-style
environment variables below (or swap the DATABASES dict) to move to
PostgreSQL in production without changing any application code.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core / security
# ---------------------------------------------------------------------------
# In production, set DJANGO_SECRET_KEY as an environment variable instead of
# relying on this fallback.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-jpi_l9)v=w7%x7x2_*h28uk(qp05_b&xd7%_ynii#$dn0()#u8',
)

# DEBUG must be False in production (controlled via env var).
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()
]

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Local apps
    'cabana',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Serves static files directly from the app process in production
    # (no separate CDN/nginx needed on Railway).
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Compresses responses (HTML/CSS/JS) for faster page loads.
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cannelle_hill.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Makes site-wide settings (phone, WhatsApp, socials, map)
                # available in every template without passing them manually.
                'cabana.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'cannelle_hill.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# SQLite for development. Swap ENGINE/credentials for PostgreSQL by setting
# the DB_* environment variables in production — no code changes required.
# ---------------------------------------------------------------------------
if os.environ.get('DB_ENGINE') == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'cannelle_hill'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # Overridable so the DB file can live on a mounted persistent
            # volume (e.g. Railway) instead of the ephemeral app filesystem.
            'NAME': os.environ.get('DJANGO_SQLITE_PATH', BASE_DIR / 'db.sqlite3'),
        }
    }

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Colombo'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = 'media/'
# Overridable so uploaded photos can live on a mounted persistent volume
# (e.g. Railway) instead of the ephemeral app filesystem.
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Email (booking / enquiry notifications)
# Falls back to console backend in development so emails print to the
# terminal instead of requiring real SMTP credentials.
# ---------------------------------------------------------------------------
if os.environ.get('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@cannellehillcabanas.com')
# Where booking/enquiry notifications are sent.
BOOKING_NOTIFICATION_EMAIL = os.environ.get('BOOKING_NOTIFICATION_EMAIL', 'reservations@cannellehillcabanas.com')

# ---------------------------------------------------------------------------
# Security hardening (relaxed automatically while DEBUG=True for local dev)
# ---------------------------------------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()
]

if not DEBUG:
    # Railway (and most PaaS hosts) terminate TLS at a proxy and forward
    # plain HTTP internally, tagging the original scheme in this header.
    # Without it, Django can't tell the request was HTTPS and
    # SECURE_SSL_REDIRECT loops forever.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

LOGIN_URL = '/admin/login/'

# ---------------------------------------------------------------------------
# Logging
# Django's own default logging silently drops request exceptions to email
# (mail_admins) once DEBUG=False, so nothing shows up in `railway logs` /
# similar. Route them to the console instead.
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
