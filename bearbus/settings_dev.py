DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bearbus_db',
        'USER': 'kat',
        'PASSWORD': 'django',
        'HOST': 'localhost',
        'PORT': '',
    }
}
