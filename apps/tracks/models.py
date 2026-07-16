from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.artists.models import Artist, Album

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Название'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks', verbose_name=_("Артист"))
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks', verbose_name=_("Альбом"))
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='tracks', verbose_name=_("Жанр"))
    audio_file = models.FileField(upload_to='tracks/', verbose_name=_("Аудио файл"))
    cover = models.ImageField(upload_to='covers/', null = True, blank=True, verbose_name=_("Обложка"))
    duration = models.IntegerField(default=0, verbose_name=_("Продолжительность"))
    plays_count = models.IntegerField(default=0, verbose_name=_("Прослушивания"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))

    class Meta:
        unique_together = ['artist', 'title']
        verbose_name = _("Трек")
        verbose_name_plural = _("Треки")
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['artist']),
            models.Index(fields=['genre'])
        ]
    
    def __str__(self):
        return self.title