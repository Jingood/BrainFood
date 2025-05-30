from django.urls import path
from . import views

urlpatterns = [
    path('api/sessions/', views.SessionListCreateView.as_view(), name='session_list_create'),
    path('api/sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('<int:pk>/', views.ChatBotPageView.as_view(), name='t_chat'),
    path('api/sessions/<int:session_id>/messages/', views.MessageCreateView.as_view(), name='message_create'),
    path('api/sessions/<int:pk>/delete/', views.ChatSessionDestroyAPIView.as_view(), name='delete_session'),
]
