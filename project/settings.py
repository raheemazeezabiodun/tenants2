"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from typing import List, Dict, Optional, Any
import dj_database_url
import dj_email_url

from . import monkeypatch_django  # noqa
from . import justfix_environment, locales
from .justfix_environment import BASE_DIR
from .util.settings_util import (
    parse_secure_proxy_ssl_header,
    parse_hostname_redirects,
    parse_comma_separated_list,
    LazilyImportedFunction,
)
from .util import git


env = justfix_environment.get()

SECRET_KEY = env.SECRET_KEY

DEBUG = env.DEBUG

# TODO: Figure out if this can securely stay at '*'.
ALLOWED_HOSTS: List[str] = ["*"]


HOSTNAME_REDIRECTS = parse_hostname_redirects(env.HOSTNAME_REDIRECTS)

if env.SECURE_PROXY_SSL_HEADER:
    SECURE_PROXY_SSL_HEADER = parse_secure_proxy_ssl_header(env.SECURE_PROXY_SSL_HEADER)

SECURE_SSL_REDIRECT = env.SECURE_SSL_REDIRECT

SECURE_HSTS_SECONDS = env.SECURE_HSTS_SECONDS

SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = env.SESSION_COOKIE_SECURE

CSRF_COOKIE_SECURE = env.CSRF_COOKIE_SECURE

# We need to set SameSite=None to allow for embedding within
# Front.  For more information, see:
#
# https://medium.com/trabe/cookies-and-iframes-f7cca58b3b9e
#
# Note that SameSite=None is only valid with secure cookies,
# though--in fact, insecure cookies with SameSite=None will
# be rejected entirely, thereby breaking the whole site, so
# we need to be careful here.
if SESSION_COOKIE_SECURE:
    SESSION_COOKIE_SAMESITE = "None"
if CSRF_COOKIE_SECURE:
    CSRF_COOKIE_SAMESITE = "None"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"

EXTENDED_HEALTHCHECK_KEY = env.EXTENDED_HEALTHCHECK_KEY

email_config = dj_email_url.parse(env.EMAIL_URL)

EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]

EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
if EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
    EMAIL_BACKEND = "project.util.friendly_email_console_backend.EmailBackend"

DEFAULT_FROM_EMAIL = env.DEFAULT_FROM_EMAIL

COURT_DOCUMENTS_EMAIL = env.COURT_DOCUMENTS_EMAIL

LOC_EMAIL = env.LOC_EMAIL

DHCR_EMAIL_SENDER_ADDRESS = env.DHCR_EMAIL_SENDER_ADDRESS
DHCR_EMAIL_RECIPIENT_ADDRESSES = env.DHCR_EMAIL_RECIPIENT_ADDRESSES.split(",")

EVICTIONFREE_REPLY_TO_EMAIL = env.EVICTIONFREE_REPLY_TO_EMAIL

NAVBAR_LABEL = env.NAVBAR_LABEL
WOW_ORIGIN = env.WOW_ORIGIN
EFNYC_ORIGIN = env.EFNYC_ORIGIN

USE_LAMBDA_HTTP_SERVER = env.USE_LAMBDA_HTTP_SERVER

FACEBOOK_APP_ID = env.FACEBOOK_APP_ID

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "graphene_django",
    "django_celery_results",
    "project.apps.DefaultConfig",
    "project.apps.JustfixAdminConfig",
    "frontend",
    "users.apps.UsersConfig",
    "hpaction.apps.HPActionConfig",
    "loc.apps.LocConfig",
    "onboarding.apps.OnboardingConfig",
    "issues.apps.IssuesConfig",
    "airtable.apps.AirtableConfig",
    "texting.apps.TextingConfig",
    "nycha.apps.NychaConfig",
    "twofactor.apps.TwofactorConfig",
    "nycdb",
    "rapidpro.apps.RapidproConfig",
    "findhelp.apps.FindhelpConfig",
    "data_requests.apps.DataRequestsConfig",
    "data_driven_onboarding.apps.DataDrivenOnboardingConfig",
    "rh.apps.RhConfig",
    "dwh.apps.DwhConfig",
    "texting_history.apps.TextingHistoryConfig",
    "docusign.apps.DocusignConfig",
    "norent.apps.NorentConfig",
    "mailchimp.apps.MailchimpConfig",
    "partnerships.apps.PartnershipsConfig",
    "evictionfree.apps.EvictionfreeConfig",
]

MIDDLEWARE = [
    "project.middleware.CSPHashingMiddleware",
    "project.middleware.hostname_redirect_middleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "twofactor.middleware.admin_requires_2fa_middleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "frontend.context_processors.safe_mode",
                "project.context_processors.ga_snippet",
                "project.context_processors.gtm_snippet",
                "project.context_processors.gtm_noscript_snippet",
                "project.context_processors.facebook_pixel_snippet",
                "project.context_processors.facebook_pixel_noscript_snippet",
                "project.context_processors.amplitude_snippet",
                "project.context_processors.fullstory_snippet",
                "project.context_processors.rollbar_snippet",
            ],
        },
    },
]

# This is like Django's SITE_ID setting, except it's used as a fallback
# rather than an authoritative identifer: if a request object isn't
# available in a particular context, we'll return this site ID, but
# otherwise we'll prefer the site that a request's domain maps to.
DEFAULT_SITE_ID = 1

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASE_ROUTERS: List[str] = []

if not env.ENABLE_FINDHELP:
    DATABASE_ROUTERS.append("findhelp.models.IgnoreFindhelpMigrationsRouter")

DATABASES = {
    "default": dj_database_url.parse(env.DATABASE_URL),
}

NYCDB_DATABASE = None

if env.NYCDB_DATABASE_URL:
    DATABASES["nycdb"] = dj_database_url.parse(env.NYCDB_DATABASE_URL)
    NYCDB_DATABASE = "nycdb"

WOW_DATABASE = None

if env.WOW_DATABASE_URL:
    DATABASES["wow"] = dj_database_url.parse(env.WOW_DATABASE_URL)
    WOW_DATABASE = "wow"

DWH_DATABASE = "default"

if env.DWH_DATABASE_URL:
    DATABASES["dwh"] = dj_database_url.parse(env.DWH_DATABASE_URL)
    DWH_DATABASE = "dwh"
    DATABASE_ROUTERS.append("dwh.dbrouter.ReadAndWriteToDataWarehouseDb")

MIGRATION_MODULES = {
    # The NYCDB is an external database that we read from, so we don't
    # want to modify its schema in any way.
    "nycdb": None
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.JustfixUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "/login"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = locales.DEFAULT

ENABLE_WIP_LOCALES = env.ENABLE_WIP_LOCALES

if ENABLE_WIP_LOCALES:
    LANGUAGES = locales.ALL.choices
else:
    LANGUAGES = locales.FULLY_SUPPORTED_ONLY.choices

LOCALE_PATHS = [str(BASE_DIR / "locales")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# This is based off the default Django logging configuration:
# https://github.com/django/django/blob/master/django/utils/log.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "rollbar": {
            # This will be replaced by a real handler if Rollbar is enabled.
            "level": "ERROR",
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "debug" if env.LOG_LEVEL == "DEBUG" else None,
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["skip_static_requests"],
            "formatter": "django.server",
        },
    },
    "filters": {
        "skip_static_requests": {
            "()": "django.utils.log.CallbackFilter",
            "callback": LazilyImportedFunction("project.logging.skip_static_requests"),
        }
    },
    "formatters": {
        "debug": {
            "format": "{levelname}:{name} {message}",
            "style": "{",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "rollbar"],
            "level": env.LOG_LEVEL,
        },
        "twilio": {
            # At the INFO level, Twilio logs the recipient and
            # body of SMS messages, which we'd like to keep out
            # of production logs, as it's PII, so we'll only
            # log warnings.
            "level": "WARNING"
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

_STATIC_ROOT_PATH = BASE_DIR / "staticfiles"

STATIC_ROOT = str(_STATIC_ROOT_PATH)

# This avoids a spurious warning from whitenoise that
# shows up even in development mode.
_STATIC_ROOT_PATH.mkdir(exist_ok=True)

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

_MEDIA_ROOT_PATH = BASE_DIR / "mediafiles"

_MEDIA_ROOT_PATH.mkdir(exist_ok=True)

MEDIA_ROOT = str(_MEDIA_ROOT_PATH)

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

if env.AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY

AWS_STORAGE_BUCKET_NAME = env.AWS_STORAGE_BUCKET_NAME

AWS_DEFAULT_ACL = "private"

AWS_BUCKET_ACL = "private"

AWS_AUTO_CREATE_BUCKET = True

AWS_STORAGE_STATICFILES_BUCKET_NAME = env.AWS_STORAGE_STATICFILES_BUCKET_NAME

AWS_STORAGE_STATICFILES_ORIGIN = f"https://{AWS_STORAGE_STATICFILES_BUCKET_NAME}.s3.amazonaws.com"

GRAPHENE = {
    "SCHEMA": "project.schema.schema",
    "SCHEMA_INDENT": 2,
    # Setting this to None is very important for error logging, as
    # its default value of
    # graphene_django.debug.middleware.DjangoDebugMiddleware somehow
    # silently eats all errors:
    #
    #   https://github.com/graphql-python/graphene-django/issues/504
    "MIDDLEWARE": None,
}

GEOCODING_SEARCH_URL = "https://geosearch.planninglabs.nyc/v1/search"

GEOCODING_TIMEOUT = 8

GA_TRACKING_ID = env.GA_TRACKING_ID

GTM_CONTAINER_ID = env.GTM_CONTAINER_ID

FACEBOOK_PIXEL_ID = env.FACEBOOK_PIXEL_ID

AMPLITUDE_API_KEY = env.AMPLITUDE_API_KEY

FULLSTORY_ORG_ID = env.FULLSTORY_ORG_ID

GIT_INFO = git.GitInfo.from_dir_or_env(BASE_DIR)

TWILIO_ACCOUNT_SID = env.TWILIO_ACCOUNT_SID

TWILIO_AUTH_TOKEN = env.TWILIO_AUTH_TOKEN

TWILIO_PHONE_NUMBER = env.TWILIO_PHONE_NUMBER

TWILIO_TIMEOUT = 10

SLACK_WEBHOOK_URL = env.SLACK_WEBHOOK_URL

SLACK_TIMEOUT = 3

AIRTABLE_API_KEY = env.AIRTABLE_API_KEY

AIRTABLE_URL = env.AIRTABLE_URL

AIRTABLE_TIMEOUT = 3

HP_ACTION_API_ENDPOINT = env.HP_ACTION_API_ENDPOINT

HP_ACTION_TEMPLATE_ID = env.HP_ACTION_TEMPLATE_ID

HP_ACTION_CUSTOMER_KEY = env.HP_ACTION_CUSTOMER_KEY

HP_ACTION_TIMEOUT = 90

TWOFACTOR_VERIFY_DURATION = env.TWOFACTOR_VERIFY_DURATION

MAPBOX_ACCESS_TOKEN = env.MAPBOX_ACCESS_TOKEN

MAPBOX_TILES_ORIGIN = "https://api.tiles.mapbox.com"

MAPBOX_TIMEOUT = 10

RAPIDPRO_API_TOKEN = env.RAPIDPRO_API_TOKEN

RAPIDPRO_HOSTNAME = env.RAPIDPRO_HOSTNAME

RAPIDPRO_FOLLOWUP_CAMPAIGN_RH = env.RAPIDPRO_FOLLOWUP_CAMPAIGN_RH
RAPIDPRO_FOLLOWUP_CAMPAIGN_LOC = env.RAPIDPRO_FOLLOWUP_CAMPAIGN_LOC
RAPIDPRO_FOLLOWUP_CAMPAIGN_HP = env.RAPIDPRO_FOLLOWUP_CAMPAIGN_HP
RAPIDPRO_FOLLOWUP_CAMPAIGN_EHP = env.RAPIDPRO_FOLLOWUP_CAMPAIGN_EHP

LOB_SECRET_API_KEY = env.LOB_SECRET_API_KEY

LOB_PUBLISHABLE_API_KEY = env.LOB_PUBLISHABLE_API_KEY

DOCUSIGN_ACCOUNT_ID = env.DOCUSIGN_ACCOUNT_ID
DOCUSIGN_INTEGRATION_KEY = env.DOCUSIGN_INTEGRATION_KEY
DOCUSIGN_USER_ID = env.DOCUSIGN_USER_ID
DOCUSIGN_AUTH_SERVER_DOMAIN = env.DOCUSIGN_AUTH_SERVER_DOMAIN
DOCUSIGN_CALLBACK_HANDLERS = [
    "hpaction.docusign.callback_handler",
]

ENABLE_EMERGENCY_HP_ACTION = env.ENABLE_EMERGENCY_HP_ACTION

MAILCHIMP_API_KEY = env.MAILCHIMP_API_KEY

MAILCHIMP_LIST_ID = env.MAILCHIMP_LIST_ID

MAILCHIMP_CORS_ORIGINS = parse_comma_separated_list(env.MAILCHIMP_CORS_ORIGINS)

FRONTAPP_PLUGIN_AUTH_SECRET = env.FRONTAPP_PLUGIN_AUTH_SECRET

IS_DEMO_DEPLOYMENT = env.IS_DEMO_DEPLOYMENT

# If this is truthy, Rollbar will be enabled on the client-side.
ROLLBAR_ACCESS_TOKEN = env.ROLLBAR_ACCESS_TOKEN

ROLLBAR: Optional[Dict[str, Any]] = None

DEBUG_DATA_DIR = env.DEBUG_DATA_DIR

if env.ROLLBAR_SERVER_ACCESS_TOKEN:
    # The following will enable Rollbar on the server-side.
    ROLLBAR = {
        "access_token": env.ROLLBAR_SERVER_ACCESS_TOKEN,
        "environment": "development" if DEBUG else "production",
        "code_version": GIT_INFO.get_version_str(),
        "root": str(BASE_DIR),
        "capture_username": True,
    }
    LOGGING["handlers"]["rollbar"].update(  # type: ignore
        {"class": "rollbar.logger.RollbarHandler"}
    )
    MIDDLEWARE.insert(0, "project.middleware.rollbar_request_middleware")
    MIDDLEWARE.append("rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404")

CSP_STYLE_SRC = [
    "'self'",
    # We originally disallowed unsafe-inline, but it just became too much of
    # a hassle, as third-party libraries injected inline styles and
    # even SVGs used in <img> tags were unable to contain <style> elements
    # too.
    "'unsafe-inline'",
]

CSP_FONT_SRC = [
    "'self'",
]

CSP_IMG_SRC = [
    "'self'",
]

CSP_SCRIPT_SRC = [
    "'self'",
]

CSP_CONNECT_SRC = ["'self'", "https://geosearch.planninglabs.nyc", "https://api.mapbox.com"]

CSP_FRAME_SRC = ["'self'", "https://www.youtube.com"]

# All settings starting with "CELERY_" are Celery
# settings. See the following documentation for more information,
# but prepend "CELERY_" to all the documented settings before
# adding them here:
#
#   https://docs.celeryproject.org/en/latest/userguide/configuration.html

CELERY_BROKER_URL = env.JUSTFIX_CELERY_BROKER_URL
CELERY_RESULT_BACKEND = "django-db"

if CELERY_BROKER_URL.startswith("amqp://"):
    # By default, using Celery with AMQP consumes *tons* of messages,
    # which quickly becomes expensive with services like CloudAMQP
    # that charge based on message usage. The following settings are
    # taken from https://www.cloudamqp.com/docs/celery.html to reduce
    # message usage and increase efficiency.

    # This will decrease connection usage.
    CELERY_BROKER_POOL_LIMIT = 1

    # We're using TCP keep-alive instead.
    CELERY_BROKER_HEARTBEAT = None

    # This may require a long timeout due to Linux DNS timeouts etc.
    CELERY_BROKER_CONNECTION_TIMEOUT = 30

    # This will delete all celeryev. queues without consumers after 1 minute.
    CELERY_EVENT_QUEUE_EXPIRES = 60

    # Disable prefetching, it causes problems and doesn't help performance.
    CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Our tasks are generally network-bound rather than CPU-bound, so we'll
# increase concurrency substantially.
CELERY_WORKER_CONCURRENCY = 5

# We want to use Django logging.
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# When executing tasks synchronously, make sure exceptions propagate.
CELERY_TASK_EAGER_PROPAGATES = True

if not CELERY_BROKER_URL:
    # If Celery integration is disabled, just execute tasks synchronously.
    CELERY_TASK_ALWAYS_EAGER = True

if AWS_STORAGE_STATICFILES_BUCKET_NAME:
    STATICFILES_STORAGE = "project.storage.S3StaticFilesStorage"
    STATIC_URL = f"{AWS_STORAGE_STATICFILES_ORIGIN}/"
    CSP_CONNECT_SRC.append(AWS_STORAGE_STATICFILES_ORIGIN)
    CSP_STYLE_SRC.append(AWS_STORAGE_STATICFILES_ORIGIN)
    CSP_FONT_SRC.append(AWS_STORAGE_STATICFILES_ORIGIN)
    CSP_SCRIPT_SRC.append(AWS_STORAGE_STATICFILES_ORIGIN)
    CSP_IMG_SRC.append(AWS_STORAGE_STATICFILES_ORIGIN)

if MAPBOX_ACCESS_TOKEN:
    CSP_IMG_SRC.append(MAPBOX_TILES_ORIGIN)

if DEBUG:
    if not env.DISABLE_DEV_SOURCE_MAPS:
        # Our development source maps use eval(), so allow its use during
        # development.
        CSP_SCRIPT_SRC.append("'unsafe-eval'")

    CSP_EXCLUDE_URL_PREFIXES = (
        # The webpack-bundle-analyzer report contains inline JS
        # that we need to permit if we want to use it, so
        # allow it during development.
        f"{STATIC_URL}frontend/report.html",
        # While the GraphIQL UI no longer has a bunch of inline
        # script code, it does retrieve many dependencies
        # from cdn.jsdelivr.net, and since we only use it
        # for development it's easiest to just disable CSP
        # on it entirely.
        "/graphiql",
    )
