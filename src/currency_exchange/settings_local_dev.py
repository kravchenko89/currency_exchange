SECRET_KEY = ...

DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = ...
EMAIL_HOST_PASSWORD = ...

CELERY_TASK_ALWAYS_EAGER = True
CELERY_ALWAYS_EAGER = ...
