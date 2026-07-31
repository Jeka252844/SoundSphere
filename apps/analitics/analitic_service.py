from django.db.models import Count
from datetime import timedelta, datetime

from apps.tracks.models import Track


class AnaliticService:
    @staticmethod
    def get_top_tracks_weekly(limit=10):
        week_ago = datetime.now() - timedelta(days=7)

        return Track.objects.filter(
            listening_history__listened_at__gte=week_ago
        ).annotate(
            weekly_plays=Count('listening_history')
        ).order_by('-weeklhy_plays')[:limit]
