# Django settings for src project.
import os

DEBUG = TEMPLATE_DEBUG = False
ADMINS = MANAGERS = []
USE_I18N = USE_L10N = False

APPEND_SLASH = True


TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'en'

SITE_ID = 1

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
WRITABLE_DIR = os.environ.get('EPIO_DATA_DIRECTORY', os.path.join(PROJECT_DIR, '..', 'data'))

STATIC_ROOT = os.path.join(PROJECT_DIR, '..', 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = '%klx3s$+!8dvkd1f-*$z3b#!ce@7l&rh5gaml#+(gvek3q296*'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, 'templates'),
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'github_auth.middleware.GithubUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
]

ROOT_URLCONF = 'project.urls'

SECURE_SSL_REDIRECT = True
SECURE_FRAME_DENY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 500

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'djangosecure',
    'floppyforms',
    'project',
    'checklists',
    'backbone_tastypie',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
]

GITHUB_CLIENT_ID = 'f273b3e2e141cd3e597c'
GITHUB_CLIENT_SECRET = 'ec845c2acf6b56231ad990afee04993fb9b30753'

try:
    from local_settings import *
except ImportError:
    pass
