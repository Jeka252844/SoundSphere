from django.contrib import admin
from .models import ListeningHistory

@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'listened_at')
    list_filter = ('listened_at',)
    date_hierarchy = 'listened_at'