import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        print('RequestLoggingMiddleware __init__')
        self.get_response = get_response

    def __call__(self, request):
        # print('RequestLoggingMiddleware __call__')
        print('RequestLoggingMiddleware __call__', request.path)
        logger.info(f"Request path: {request.path}")
        response = self.get_response(request)
        return response
    



