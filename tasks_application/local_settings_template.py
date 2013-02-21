# -*- coding: utf-8 *-*

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3'
        # or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': 'ddbb.db',
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

HOME_URL = '/'
LOGIN_REDIRECT_URL = HOME_URL
LOGIN_URL = HOME_URL + '/accounts/login/'

SESSION_COOKIE_NAME = 'tasks'
