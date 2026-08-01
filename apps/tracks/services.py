from django.db.models import Count
from datetime import timedelta, datetime

from apps.tracks.models import Track


class TrackService:
    @staticmethod
    def get_top_tracks_weekly(limit=10):
        week_ago = datetime.now() - timedelta(days=7)

        return Track.objects.filter(
            listening_history__listened_at__gte=week_ago
        ).annotate(
            weekly_plays=Count('listening_history')
        ).order_by('-weekly_plays')[:limit]

    @staticmethod
    def search_track(query='', genre_name=None, artist_name=None, page=1, limit=50):
        offset = (page - 1) * limit
        qs = Track.objects.all()
        if query:
            qs = qs.filter(title__icontains=query)
        if genre_name:
            qs = qs.filter(genre__name=genre_name)
        if artist_name:
            qs = qs.filter(artist__name__icontains=artist_name)
        return qs.order_by('-plays_count')[offset:offset + limit]
