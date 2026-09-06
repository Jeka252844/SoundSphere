from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class ListeningHistory(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='listening_history',
        null=True, blank=True,
        verbose_name=_('пользователь'))
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE, related_name='listening_history', verbose_name=_('трек'))
    listened_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата прослушивания'))

    class Meta:
        ordering = ['-listened_at']
        verbose_name = _('История прослушиваний')
        verbose_name_plural = _('История прослушиваний')

    def __str__(self):
        return f'{self.track.title} — {self.listened_at}'


class DailyTrackStats(models.Model):
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE, related_name='daily_stats')
    date = models.DateField(verbose_name=_('день'))
    plays = models.IntegerField(default=0, verbose_name=_('прослушивания'))
    likes = models.IntegerField(default=0, verbose_name=_('лайки'))

    class Meta:
        verbose_name = _("Дневная статистика")
        verbose_name_plural = _("Дневные статистики")
        unique_together = ['track', 'date']


class ShareToken(models.Model):
    user = models.ForeignKey('users.User', related_name='share_token', on_delete=models.CASCADE , verbose_name=_('пользователь'))
    token = models.UUIDField(default=uuid4, unique=True, verbose_name=_('Токен'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Время создания"))
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))

    class Meta:
        verbose_name = _("Токен")
        verbose_name_plural = _("Токены")

    def __str__(self):
        return f'{self.user.name} shared token'

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class DailyStats(models.Model):
    user = models.ForeignKey('users.User', related_name='daily_stats', on_delete=models.CASCADE , verbose_name=_('пользователь'))
    date = models.DateField(verbose_name=_('дата'))
    listens_count = models.IntegerField(default=0, verbose_name=_('колличество прослушиваний'))
    unique_tracks = models.IntegerField(default=0, verbose_name=_('Колличество треков'))
    total_duration = models.IntegerField(default=0, verbose_name=_('время прослушивания'))

    class Meta:
        verbose_name = _("Дневная статистика")
        verbose_name_plural = _("Дневные статистики")