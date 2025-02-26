import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers
import logging


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ride_proj.settings")
logging.basicConfig(level=logging.DEBUG)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/drivers/", consumers.DriverConsumer.as_asgi()),
                ]
            )
        ),
    }
)
