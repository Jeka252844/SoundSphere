from django.db import models

class Report(models.Model):
    REPORT_TYPES = [
        ('track', 'Трек'),
        ('album', 'Альбом'),
        ('artist', 'Артист'),
    ]
    
    type = models.CharField(max_length=20, choices=REPORT_TYPES)
    target_id = models.IntegerField()
    reason = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    reporter = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return f'{self.get_type_display()} #{self.target_id}'