from django.urls import path

from apps.social.views import ReportCreateAPIView

urlpatterns = [
    path('report/', ReportCreateAPIView.as_view(), name='report-create'),
]