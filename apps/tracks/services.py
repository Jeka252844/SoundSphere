from apps.tracks.models import Track

class TrackService:
    @staticmethod
    def get_top_by_genre(genre_name, page = 1, limit = 50):
        offset = (page-1) * limit
        return Track.objects.filter(
            genre__name=genre_name
        ).order_by('-plays_count')[offset:offset + limit]

    @staticmethod
    def get_top_tracks(page = 1, limit = 50):
        offset = (page-1) * limit
        return Track.objects.order_by('-plays_count')[offset:offset + limit]
    
    @staticmethod
    def search_track(query='', genre_name=None, artist_name=None, page=1, limit=50):
        offset = (page-1) * limit
        qs = Track.objects.all()
        if query:
            qs = qs.filter(title__icontains=query)
        if genre_name:
            qs = qs.filter(genre__name=genre_name)
        if artist_name:
            qs = qs.filter(artist__name__icontains=artist_name)
        return qs.order_by('-plays_count')[offset:offset + limit]