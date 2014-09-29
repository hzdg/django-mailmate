SECRET_KEY = 'SEKRIT'

INSTALLED_APPS = ('tests', 'mailmate')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests/mailmate.db'
    }
}
