from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('register/', views.register_view, name='register'),
]
