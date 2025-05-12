from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('api/login/', views.CookieTokenObtainPairView.as_view(), name='login'),
    path('api/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_change/', views.PasswordChangeAPIView.as_view(), name='password_change'),
    path('api/delete/', views.DeleteAccountAPIView.as_view(), name='delete_account'),
]