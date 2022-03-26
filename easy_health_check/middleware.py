from django.http import HttpResponse
from .settings import health_check_settings


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == health_check_settings.PATH:
            response = HttpResponse(health_check_settings.RETURN_BYTE_DATA)
            response.status_code = health_check_settings.RETURN_STATUS_CODE
            return response

        return self.get_response(request)
