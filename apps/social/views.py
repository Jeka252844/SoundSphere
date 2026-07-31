from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.social.models import Report


class ReportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Report.objects.create(
            type=request.data.get('type'),
            target_id=request.data.get('target_id'),
            reason=request.data.get('reason'),
            description=request.data.get('description', ''),
            reporter=request.user
        )
        return Response({'status': 'ok'})
