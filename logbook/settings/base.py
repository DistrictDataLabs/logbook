# logbook.settings.base
# The common Django settings for LogBook project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:17:27 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: base.py [] bbengfort@districtdatalabs.com $

"""
Django settings for LogBook project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.conf import global_settings

##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)

##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY = os.path.dirname(PROJECT)

##########################################################################
## Secret settings - do not store!
##########################################################################

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

## See https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'logbook'),
        'USER': environ_setting('DB_USER', 'django'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

##########################################################################
## Runtime settings
##########################################################################

## Debugging settings
## SECURITY WARNING: don't run with debug turned on in production!
DEBUG          = True

## Hosts
ALLOWED_HOSTS  = ["*"]
INTERNAL_IPS   = ('127.0.0.1', '198.168.1.10')

## WSGI Configuration
ROOT_URLCONF     = 'logbook.urls'
WSGI_APPLICATION = 'logbook.wsgi.application'

## Application definition
INSTALLED_APPS = (
    # Django apps
    'grappelli', # Must come before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    # 'social.apps.django_app.default',
    # 'rest_framework',
    'storages',
    'django_gravatar',

    # LogBook apps
)

## Request Handling
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

## Internationalization
## https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

## Admin Title
GRAPPELLI_ADMIN_TITLE = "LogBook Admin"

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

## Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social.apps.django_app.context_processors.backends',
            ],
        },
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    os.path.join(PROJECT, 'assets'),
)

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'bbengfort@districtdatalabs.com'),
    ('Tony Ojeda', 'tojeda@districtdatalabs.com'),
)

SERVER_EMAIL    = 'Dakota <server@bengfort.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER = 'server@bengfort.com'
EMAIL_HOST_PASSWORD  = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587
EMAIL_SUBJECT_PREFIX = '[LOGBOOK] '

##########################################################################
## Authentication
##########################################################################

LOGIN_URL = '/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/app'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Google OAuth2 Credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    = environ_setting("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_SECRET")
