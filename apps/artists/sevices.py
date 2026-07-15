from django.db.models import Count

from apps.artists.models import Artist

class ArtistService:
    @staticmethod
    def get_top_artists(page=1, limit=50):
        offset = (page-1) * limit
        return Artist.objects.annotate(
            followers_count = Count('follower')
        ).order_by('-followers_count')[offset:offset + limit]
    
    @staticmethod
    def search_artist(query='', page = 1, limit = 50):
        offset = (page-1) * limit
        return Artist.objects.filter(name__icontains = query).annotate(
            followers_count = Count('follower')
        ).order_by('-followers_count')[offset:offset + limit]
    
