from currency_exchange.settings import *

SECRET_KEY = 'lqnc3q63(uf&b&=%v2vql=+gukpwhi8tg*g!)fj3e8*xet790='

DEBUG = False
ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = CELERY_TASK_ALWAYS_EAGER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.outbox'
