from django.conf import settings

from bokchoy.utils.log import base_logger
from bokchoy.utils.imports import get_instance


serializer = get_instance(settings.BOKCHOY_SERIALIZER_CLASS)

result = get_instance(settings.BOKCHOY_RESULT_BACKEND_CLASS)

conductor = get_instance(settings.BOKCHOY_BACKEND_CLASS,
                         serializer=serializer,
                         logger=base_logger,
                         result=result,
                         tcp_addresses=settings.BOKCHOY_TCP_ADDRESSES,
                         http_addresses=settings.BOKCHOY_HTTP_ADDRESSES)
