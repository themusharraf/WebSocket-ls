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
