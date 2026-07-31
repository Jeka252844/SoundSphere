from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.analitics.models import ListeningHistory

class CurrentListeningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last = ListeningHistory.objects.filter(
            user=request.user
        ).order_by('-listened_at').first()
        
        if last:
            return Response({'track_id': last.track.id})
        return Response({'track_id': None})