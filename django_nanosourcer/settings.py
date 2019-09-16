# # -*- coding: UTF-8 -*-

# Django settings for django-nanosourcer project.

import os
import re


from django.http import HttpRequest

from nanosourcer_lti_helper.nanosourcer_lti_app_config import NanoSourcerLtiAppConfig

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

APPEND_SLASH = True

SERVER_ENV = os.getenv('UTLS_SERVER_ENV')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_APP_URL = "/"

APP_NAME = "django_nanosourcer"

PROJECT_ROOT = "{0}/{1}".format(BASE_DIR, APP_NAME)

DEBUG = True
# TEMPLATE_DEBUG = DEBUG

DEFAULT_SESSION_EXPIRY = 3600

SECURE_SSL_REDIRECT = False

CSRF_COOKIE_HTTPONLY = False if os.getenv('UTLS_CSRF_COOKIE_HTTPONLY') == 'false' else True
CSRF_COOKIE_SECURE = False if os.getenv('UTLS_CSRF_COOKIE_SECURE') == 'false' else True
CSRF_TRUSTED_ORIGINS = [

    'utexas.instructure.com'

]
SESSION_COOKIE_HTTPONLY = False if os.getenv('UTLS_SESSION_COOKIE_HTTPONLY') == 'false' else True
SESSION_COOKIE_SECURE = False if os.getenv('UTLS_SESSION_COOKIE_SECURE') == 'false' else True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

GAZETTEER_BASE_URL = os.getenv('UTLS_GLS_API_BASE_URL')
GAZETTEER_API_KEY = os.getenv('UTLS_GLS_API_KEY')

MAPBOX_URL = os.getenv('LAITS_MAPBOX_NANOSOURCER_URL')
MAPBOX_TOKEN = os.getenv('LAITS_MAPBOX_NANOSOURCER_TOKEN')
MAPBOX_LEAFLET_URL = os.getenv('LAITS_MAPBOX_NANOSOURCER_LEAFLET_URL')


# ========================================================================================
# Section for initiating LTI objects, and database connection.
# Requires environment variables to be present for app at runtime.

middleware_exclude_paths = [

    re.compile('^/$'),
    re.compile('^[/]?favicon.ico.*$'),
    re.compile('^/config/.*$')

]

if SERVER_ENV == "LOCAL":

    middleware_exclude_paths.append(re.compile('^/test-student-view/$'))
    middleware_exclude_paths.append(re.compile('^/update-hash/$'))


lti_config_dict = {'lti_host_key': os.getenv('UTLS_LTI_HOST_KEY'),
                   'lti_consumer_key': os.getenv('UTLS_LTI_CONSUMER_KEY'),
                   'lti_consumer_secret': os.getenv('UTLS_LTI_CONSUMER_SECRET'),
                   'lti_encryption_pass_key': os.getenv('UTLS_LTI_ENCRYPTION_PASS_KEY'),
                   'lti_middleware_exclude_paths': middleware_exclude_paths
                   }

extra_headers = {}

LTI_APP_CONFIG = NanoSourcerLtiAppConfig(lti_config_dict,
                                         debug=False,
                                         headers=extra_headers)

FEDORA_ROOT = os.getenv('UTLS_FEDORA_ROOT')
FEDORA_USER = os.getenv('UTLS_FEDORA_USER')
FEDORA_PASSWORD = os.getenv('UTLS_FEDORA_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('UTLS_DB_NAME'),
        'USER': os.getenv('UTLS_DB_USER'),
        'PASSWORD': os.getenv('UTLS_DB_PASSWORD'),
        'HOST': os.getenv('UTLS_DB_HOST'),
        'PORT': ''
    }
}

# Mapping of Canvas named roles to application keys.
SERVICE_ROLE_MAPPINGS = {'TeacherEnrollment': 'instructor',
                         'Instructor': 'instructor',
                         'TeachingAssistant': 'ta',
                         'TaEnrollment': 'ta',
                         'Administrator': 'admin',
                         'StudentEnrollment': 'student',
                         'Learner': 'student'}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

HOME_ROOT = os.path.dirname(__file__)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..//', 'django_nanosourcer/static').replace('\\', '/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (


)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('UTLS_DJANGO_SECRET_KEY')

MIDDLEWARE_CLASSES = (
    # 'site_maintenance.middleware.site_maintenance_middleware.SiteMaintenanceMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nanosourcer_lti_helper.nanosourcer_lti_middleware.NanoSourcerLtiHandshakeMiddleware',
)

ROOT_URLCONF = 'django_nanosourcer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_nanosourcer.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(os.path.dirname(__file__), '../', 'django_nanosourcer/templates').replace('\\', '/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.request",
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': os.getenv('UTLS_DJANGO_TEMPLATE_DEBUG'),
        },
    },
]

if SERVER_ENV == "LOCAL":

    import sslserver

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        'nanosourcer_lti_helper',
        'sslserver',
        'django_nanosourcer',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
    )

else:

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        'nanosourcer_lti_helper',
        'django_nanosourcer',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
    )


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s: %(levelname)s: %(module)s: %(process)d: %(thread)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s: %(levelname)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'app_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "{0}/log/main.log".format(BASE_DIR),
            'maxBytes': os.getenv('UTLS_LOG_MAXBYTES_PER_FILE'),
            'backupCount': os.getenv('UTLS_LOG_BACKUP_COUNT'),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'main': {
            'handlers': ['app_logfile'],
            'level': 'DEBUG',
        },
    }
}
