from django.contrib import admin
from apps.social.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('type', 'target_id', 'reason', 'reporter', 'created_at', 'resolved')
    list_filter = ('type', 'resolved')