import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'f)!nw+q&3@^28c5lj8h+9*cn%hj%(143@*mj5l21iebgl2rpg2'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    	'data',
    )