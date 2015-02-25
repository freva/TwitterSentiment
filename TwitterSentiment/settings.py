import os
import socket
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEFAULT_SECRET_KEY = '3iy-!-d$!pc_ll$#$elg&cpr@*tfn-d5&n9ag=)%#()t$$5%5^'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

if '3883' in socket.gethostname():
    DEBUG = TEMPLATE_DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':'tweets',
            'USER':'admin',
            'PASSWORD':'asdqwe123',
            'HOST':'185.69.55.87',
            'PORT':'3306',
        }
    }
else:
    DEBUG = TEMPLATE_DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_ajax',

    'TwitterSentiment.scraper',
    'TwitterSentiment.frontpage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'TwitterSentiment/templates'),
)

ROOT_URLCONF = 'TwitterSentiment.urls'
WSGI_APPLICATION = 'TwitterSentiment.wsgi.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)