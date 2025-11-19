from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/ia/', views.chat_ia, name='chat_ia'),
]