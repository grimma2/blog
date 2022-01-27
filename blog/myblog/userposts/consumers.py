import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Comment, Video


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.video_name = 'my_group_%s' % self.video_id

        await self.channel_layer.group_add(
            self.video_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.discard(
            self.video_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']
        new_comment = await self.create_new_comment(comment)
        data = {'author': new_comment.author.username,
                'text': new_comment.text}
        # Send message to room group
        await self.channel_layer.group_send(
            self.video_name,
            {
                'type': 'new_comment',
                'message': data
            }
        )

    # Receive message from room group
    async def new_comment(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_comment(self, text):
        new_comment = Comment.objects.create(
            user=self.scope['user'],
            text=text,
            content_object=Video.objects.get(slug=self.video_slug)
        )
        return new_comment
