from ..settings.common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lair6Vol6sarieyaiquueJ8mooH4raineeheixooCh3ohvah6Vepail8ohl1nah2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "*"
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'isp_identity_store',
        'USER': 'isp_identity_store',
        'PASSWORD': 'caez9Ir1doo4Eevoo7uu7iCeng2iepoo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}