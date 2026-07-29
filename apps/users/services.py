from django.db.models import Count
from datetime import datetime, timedelta
import time

from apps.users.models import PlayList

class UserService:
    @staticmethod
    def delete_unverified_user(user_id):
        time.sleep(300)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id, is_active=False)
            user.delete()
        except User.DoesNotExist:
            pass

class PlaylistService:
    @staticmethod
    def top_weekly_playlists():
        one_week_ago = datetime.now() - timedelta(days=7)

        return PlayList.objects.filter(
            playlist_like__liked_at__gte=one_week_ago
        ).annotate(
            weekly_likes=Count('playlist_like')
        ).order_by('-weekly_likes')[:4]