from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:username>/', views.chat_view, name='private_chat'),
]
