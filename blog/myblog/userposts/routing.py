from django.urls import re_path

from .consumers import CommentsConsumer


websocket_urlpatterns = [
    re_path(r'videos/(?P<video_slug>\d+)/$', CommentsConsumer.as_asgi()),
]
