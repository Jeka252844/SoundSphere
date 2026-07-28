from django.db.models import Count
from datetime import datetime, timedelta

from apps.users.models import PlayList

class PlaylistService:
    @staticmethod
    def top_weekly_playlists():
        one_week_ago = datetime.now() - timedelta(days=7)

        return PlayList.objects.filter(
            playlist_like__liked_at__gte=one_week_ago
        ).annotate(
            weekly_likes=Count('playlist_like')
        ).order_by('-weekly_likes')[:4]