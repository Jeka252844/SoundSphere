from django.db import models

class ListeningHistory(models.Model):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='listening_history', 
        null=True, blank=True,
        verbose_name='пользователь')
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE, related_name='listening_history',verbose_name='трек')
    listened_at = models.DateTimeField(auto_now_add=True, verbose_name='дата прослушивания')

    class Meta:
        ordering = ['-listened_at']
        verbose_name = 'История прослушиваний'
        verbose_name_plural = 'История прослушиваний'

    def __str__(self):
        return f'{self.track.title} — {self.listened_at}'
    

class DailyStats(models.Model):
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE, related_name='daily_stats')
    date = models.DateField()
    plays = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['track', 'date']