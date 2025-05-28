from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserInfoAPIView.as_view(), name='userinfo'),
    path('api/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('signup/', views.SignupPageView.as_view(), name= 't_signup'),
    path('api/login/', views.CookieTokenObtainPairView.as_view(), name='login'),
    path('login/', views.LoginPageView.as_view(), name='t_login'),
    path('api/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_change/', views.PasswordChangeAPIView.as_view(), name='password_change'),
    path('api/delete/', views.DeleteAccountAPIView.as_view(), name='delete_account'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/', views.ProfilePageView.as_view(), name='t_profile'),
]