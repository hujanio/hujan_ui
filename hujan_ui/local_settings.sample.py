from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MAAS_API_KEY = ""
MAAS_URL = ""
WITH_EX_RESPONSE = False