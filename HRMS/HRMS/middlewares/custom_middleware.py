# custom_middleware.py
from django.utils.deprecation import MiddlewareMixin

class BypassCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Bypass CSRF for the specific login endpoint
        print('custom middleware called!')
        if request.path == '/login/authenticate/':
            setattr(request, '_dont_enforce_csrf_checks', True)
