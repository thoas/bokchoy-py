from django.conf import settings

from bokchoy.utils.log import base_logger
from bokchoy.utils.imports import get_instance


serializer = get_instance(settings.BOKCHOY_SERIALIZER)

result = get_instance(settings.BOKCHOY_RESULT,
                      **settings.BOKCHOY_RESULT_OPTIONS)

conductor = get_instance(settings.BOKCHOY_CONDUCTOR,
                         serializer=serializer,
                         logger=base_logger,
                         result=result,
                         **settings.BOKCHOY_CONDUCTOR_OPTIONS)
