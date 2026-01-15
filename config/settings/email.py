from config.settings.base import *

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.environ["EMAIL_HOST"],
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"],
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"],
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 300
DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"],