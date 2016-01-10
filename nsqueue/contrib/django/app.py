from django.conf import settings

from nsqueue.utils.log import base_logger
from nsqueue.utils.imports import get_instance


serializer = get_instance(settings.NSQUEUE_SERIALIZER_CLASS)

result = get_instance(settings.NSQUEUE_RESULT_BACKEND_CLASS)

conductor = get_instance(settings.NSQUEUE_BACKEND_CLASS,
                         serializer=serializer,
                         logger=base_logger,
                         result=result,
                         tcp_addresses=settings.NSQUEUE_TCP_ADDRESSES,
                         http_addresses=settings.NSQUEUE_HTTP_ADDRESSES)
