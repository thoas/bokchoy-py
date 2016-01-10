from django.conf import settings as djsettings


ALWAYS_EAGER = getattr(djsettings, 'NSQUEUE_ALWAYS_EAGER', False)
DEFAULT_TOPIC = getattr(djsettings, 'NSQUEUE_DEFAULT_TOPIC', 'default')
DEFAULT_RESULT_TTL = getattr(djsettings, 'NSQUEUE_DEFAULT_RESULT_TTL', 86400)
DEFAULT_RETRY_INTERVAL = getattr(djsettings, 'NSQUEUE_DEFAULT_RETRY_INTERVAL', 180)
DEFAULT_MAX_RETRIES = getattr(djsettings, 'NSQUEUE_DEFAULT_MAX_RETRIES', 0)
