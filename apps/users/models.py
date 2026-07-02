from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_("Аватар"))
    bio = models.TextField(max_length=300, blank=True, verbose_name=_('Биография'))
    is_artist = models.BooleanField(default=False, verbose_name=_('Артист'))

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['is_artist'])
        ]
        ordering = ['-date_joined']


class PlayList(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название плэйлиста"))
    user = models.ForeignKey(User, related_name='playlist', on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    is_public = models.BooleanField(default=True, verbose_name=_("Публичный"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    class Meta:
        verbose_name = _("Плэйлист")
        verbose_name_plural = _("Плайлисты")
        indexes = [
            models.Index(fields=['user', '-created_at'])
        ]
        ordering = ['-created_at']

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name=_('Подписчик'))
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name=_("Подписан на"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    class Meta:
        verbose_name = _("Подписчик")
        verbose_name_plural = _("Подписчики")
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following'])
        ]
        ordering = ['-created_at']