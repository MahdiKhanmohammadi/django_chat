from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/room/<pk>/", ChatConsumer.as_asgi())
]
