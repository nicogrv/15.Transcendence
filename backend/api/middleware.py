from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import asyncio
from asgiref.sync import sync_to_async, async_to_sync

class AuthorizationHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get("access")
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        
    def process_response(self, request, response):
        csrf_token = request.COOKIES.get("csrftoken")
        response["X-CSRFToken"] = csrf_token
    
        if response.status_code == 401:
            refresh_token = request.COOKIES.get("refresh")
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                        value=new_access_token,
                        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    )
                    response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
                    retry_response = async_to_sync(self.retry_request)(request, new_access_token)
                    if retry_response.status_code != 401:
                        return retry_response
                    else:
                        return response
                except Exception as e:
                    response = JsonResponse({'message': 'Token refresh failed'}, status=401)
        return response

    async def retry_request(self, request, new_access_token):
        request.COOKIES['access'] = new_access_token
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
        response = self.get_response(request)
        if asyncio.iscoroutine(response):
            response = await response
        return response
