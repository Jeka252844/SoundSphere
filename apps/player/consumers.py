from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import asyncio
import os

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

        ext = track.audio_file.name.split('.')[-1].lower()
        mime_map = {
            'mp3': 'audio/mpeg',
            'ogg': 'audio/ogg',
            'wav': 'audio/wav',
            'flac': 'audio/flac',
        }
        mime_type = mime_map.get(ext, 'audio/mpeg')

        try:
            await self.send(text_data=json.dumps({
                "type": "metadata",
                "duration": track.duration,
                "mime_type": mime_type
            }))

            file_path = track.audio_file.path
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as f:
                file_data = f.read()

            chunk_size = 16384
            offset = 0
            
            while offset < file_size:
                chunk = file_data[offset:offset + chunk_size]
                await self.send(bytes_data=chunk)
                offset += chunk_size
                await asyncio.sleep(0.05)
            
            await asyncio.sleep(1.0)
            await self.send(text_data=json.dumps({'type': 'end_of_stream'}))

        except Exception as e:
            await self.send(text_data=json.dumps({"type": "error", "message": str(e)}))