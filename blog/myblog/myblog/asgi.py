import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from userposts import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
        routing.websocket_urlpatterns
        )
    )
})