#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from wger.settings_global import *  # noqa
import dj_database_url

# Use 'DEBUG = True' to get more details for server errors
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True  # noqa

ADMINS = (
    ('Your name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT")
    }
}
if os.environ.get("TRIGGER") == "True":
    DATABASES["default"] = dj_database_url.config()


# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

# fitbit keyS
FITAPP_CLIENT_ID = os.environ.get("CLIENT_ID")
FITAPP_CONSUMER_KEY = os.environ.get("CLIENT_SECRET")
FITAPP_CALLBACK_URL = os.environ.get("CALLBACK_URL")

# Your reCaptcha keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True

# The site's URL (e.g. http://www.my-local-gym.com or http://localhost:8000)
# This is needed for uploaded files and images (exercise images, etc.) to be
# properly served.
SITE_URL = os.environ.get("SITE_URL")

# Path to uploaded files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/wger/media'
MEDIA_URL = '/media/'

# Allow all hosts to access the application. Change if used in production.
ALLOWED_HOSTS = '*'

# This might be a good idea if you setup memcached
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configure a real backend in production
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sender address used for sent emails
WGER_SETTINGS['EMAIL_FROM'] = 'wger Workout Manager <wger@example.com>'  # noqa

# Your twitter handle, if you have one for this instance.
# WGER_SETTINGS['TWITTER'] = ''
