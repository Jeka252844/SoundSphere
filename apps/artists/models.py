from django.db import models
from django.utils.translation import gettext_lazy as _

class Artist(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Имя"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("Биография"))
    avatar = models.ImageField(upload_to='artists/', null=True, blank=True, verbose_name=_("Аватар"))
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='artist', null=True, verbose_name=_("Пользователь"))

    class Meta:
        verbose_name = _("Исполнитель")
        verbose_name_plural = _("Исполнители")
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("Название"))
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', verbose_name=_("Исполнитель"))
    cover = models.ImageField(upload_to='albums/', null=True, blank=True, verbose_name=_("Обложка"))
    release_date = models.DateField(null=True, blank=True, verbose_name=_("Релиз"))

    class Meta:
        verbose_name = _("Альбом")
        verbose_name_plural = _("Альбомы")
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['artist'])
        ]
    
    def __str__(self):
        return self.title