import os
import django

django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP uchun ASGI application # noqa
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # WebSocket routing
        )
    ),
})

"""
http://127.0.0.1:8000/chat/john/ — admin user bu sahifaga kirsa, admin <-> john xonasi ochiladi.
WebSocket URL bo‘ladi: ws://127.0.0.1:8000/ws/chat/john/
Faqat 2 foydalanuvchi o‘rtasida chat ishlaydi (admin, john) va boshqa hech kim kira olmaydi
"""  # noqa
