from django.conf import settings as djsettings

from bokchoy import defaults


ALWAYS_EAGER = getattr(djsettings, 'BOKCHOY_ALWAYS_EAGER', False)
QUEUE = getattr(djsettings, 'BOKCHOY_DEFAULT_QUEUE', 'default')
TTL = getattr(djsettings, 'BOKCHOY_DEFAULT_TTL', defaults.TTL)
RETRY_INTERVAL = getattr(djsettings, 'BOKCHOY_DEFAULT_RETRY_INTERVAL', defaults.RETRY_INTERVAL)
MAX_RETRIES = getattr(djsettings, 'BOKCHOY_DEFAULT_MAX_RETRIES', defaults.MAX_RETRIES)
TIMEOUT = getattr(djsettings, 'BOKCHOY_DEFAULT_TIMEOUT', defaults.TIMEOUT)
