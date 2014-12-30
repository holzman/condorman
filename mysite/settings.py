# Django settings for mysite project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DJ_ROOT = '/var/lib/djangoapp'
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'condorman',
        'USER': 'condoradmin',
        'PASSWORD': 'NOT_THE_ACTUAL_PW',
        'HOST': '',
        'PORT': '',
        }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True

STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = '%s/mysite/media/' % DJ_ROOT
MEDIA_URL = 'http://localhost:8000/media/'
STATIC_URL = '/media-admin/'

# Make this unique, and don't share it with anybody.


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

AUTHENTICATION_BACKENDS = (

# NB: I had my DOEGrids cert expire.  To log in to the admin site (/condorman/admin),
# might need to uncomment ModelBackend (and maybe comment MyBackend) and restart httpd.
    
#    'django.contrib.auth.backends.RemoteUserBackend',
#    'django.contrib.auth.backends.ModelBackend',
    'condorman.auth.MyBackend',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % DJ_ROOT
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
#    'polls',
    'condorman',
    'reversion'
)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import settings_local
DATABASES['default']['PASSWORD'] = settings_local.passwords['default']
SECRET_KEY = settings_local.secret_key

# There should be a file NOT in git called settings_local.py in this dir
# with the following lines:
#
# passwords = { 'default': 'CHANGEME' }
# secret_key = 'CHANGEME2'

# CHANGEME is the password for the condoradmin user
# secret_key is a key for internal Django use
