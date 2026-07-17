from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from apps.tracks.models import Track

class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"type": "connect", "status": "ready"}))
    
    async def disconnect(self, code: int):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')

        if command == 'play':
            track_id = data['track_id']
            await self.stream_track(track_id)

        elif command == 'pause':
            await self.send(text_data=json.dumps({"type": 'pause'}))

        elif command == 'seek':
            position = data.get('position', 0)
            await self.send(text_data=json.dumps({'type': "seeked", 'position': position}))
        
    async def stream_track(self, track_id):
        track = await database_sync_to_async(Track.objects.get)(id=track_id)
        if not track.audio_file:
            await self.send(text_data=json.dumps({"type": "error", "message": "No audio file"}))
            return
        with open(track.audio_file.path, 'rb') as f:
            while chunk := f.read(8192):
                await self.send(bytes_data=chunk)