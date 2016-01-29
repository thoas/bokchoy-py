from django.conf import settings

CACHE_ALIAS = getattr(settings, 'BOKCHOY_REDIS_CACHE_ALIAS', 'bokchoy')
