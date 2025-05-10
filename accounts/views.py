from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import SignupSerializer
from datetime import timedelta

COOKIE_MAX_AGE = int(timedelta(days=1).total_seconds())

class SignupAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        access, refresh = data['access'], data['refresh']

        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            access,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )

        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            refresh,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            path='/api/refresh/',
        )
        response.data = {'detail': 'login success'}
        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        )
        response = super().post(request, *args, **kwargs)
        new_access = response.data['access']

        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            new_access,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )
        response.data = {'detail': 'token refreshed'}
        return response

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_cookie_name = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        refresh_token_raw = request.COOKIES.get(refresh_cookie_name)

        if refresh_token_raw:
            try:
                token = RefreshToken(refresh_token_raw)
                token.blacklist()
            except (TokenError, AttributeError):
                pass
        
        response = Response({'detail': 'logout success'}, status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            path='/',
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        response.delete_cookie(
            refresh_cookie_name,
            path='/api/refresh/',
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        return response