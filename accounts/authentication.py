from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError, AuthenticationFailed):
            request._force_delete_jwt = True 
            return None
        
        return self.get_user(validated_token), validated_token