from django.urls import re_path

from .consumers import *


websocket_urlpatterns = [
    re_path('ws/socket-chat/(?P<chat_pk>\d+)/(?P<username>\w+)/$', ChatConsumer.as_asgi())
]
