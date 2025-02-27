import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
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
                    re_path(
                        r"ws/drivers/(?P<driver_id>\w+)/$",
                        consumers.DriverConsumer.as_asgi(),
                    ),
                ]
            )
        ),
    }
)
