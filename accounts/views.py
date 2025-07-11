from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import SignupSerializer, PasswordChangeSerializer
from chat.models import ChatSession
from chat.serializers import ChatSessionListSerializer
from datetime import timedelta


User = get_user_model()
COOKIE_MAX_AGE = int(timedelta(days=1).total_seconds())


class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"username": user.username}, status=status.HTTP_200_OK)


class SignupAPIView(CreateAPIView):
    authentication_classes: tuple = ()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer


class SignupPageView(TemplateView):
    template_name = "accounts/signup.html"


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
            path='/',
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
        response.data = {'detail': "login success"}
        return response


class LoginPageView(TemplateView):
    template_name = "accounts/login.html"


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
        response.data = {'detail': "token refreshed"}
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
        
        response = Response({'detail': "logout success"}, status=status.HTTP_204_NO_CONTENT)

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


class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)


class PasswordChangePageView(TemplateView):
    template_name = "accounts/password_change.html"


class DeleteAccountAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], path='/api/refresh/')
        response.data = {'detail': "account deleted"}
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        sessions_qs = (
            ChatSession.objects.filter(user=user).order_by("-created_at")
        )

        sessions_ser = ChatSessionListSerializer(sessions_qs, many=True)

        data = {
            "username": user.username,
            "nickname": user.nickname,
            "sessions": sessions_ser.data,
        }
        return Response(data)


class ProfilePageView(TemplateView):
    template_name = "accounts/profile.html"