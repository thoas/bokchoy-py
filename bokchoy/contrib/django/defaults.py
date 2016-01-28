from django.conf import settings as djsettings


ALWAYS_EAGER = getattr(djsettings, 'BOKCHOY_ALWAYS_EAGER', False)
DEFAULT_TOPIC = getattr(djsettings, 'BOKCHOY_DEFAULT_TOPIC', 'default')
DEFAULT_RESULT_TTL = getattr(djsettings, 'BOKCHOY_DEFAULT_RESULT_TTL', 86400)
DEFAULT_RETRY_INTERVAL = getattr(djsettings, 'BOKCHOY_DEFAULT_RETRY_INTERVAL', 180)
DEFAULT_MAX_RETRIES = getattr(djsettings, 'BOKCHOY_DEFAULT_MAX_RETRIES', 0)
