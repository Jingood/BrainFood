import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        cookies = {}
        for header, value in scope["headers"]:
            if header == b"cookie":
                for pair in value.decode().split(";"):
                    if "=" in pair:
                        k, v = pair.strip().split("=", 1)
                        cookies[k] =v
        raw_token = cookies.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        user = AnonymousUser()
        if raw_token:
            try:
                validated = self.jwt_auth.get_validated_token(raw_token)
                user = await database_sync_to_async(self.jwt_auth.get_user)(validated)
            except Exception:
                pass
        
        scope["user"] = user
        return await self.inner(scope, receive, send)


class ClearInvalidJWT:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        if getattr(request, "_force_delete_jwt", False):
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"], path="/")
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"], path="/api/refresh/")
        return response