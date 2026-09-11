from celery import shared_task
from django.utils import timezone
from .models import ShareToken


@shared_task
def cleanup_expired_tokens():
    deleted, _ = ShareToken.objects.filter(
        expires_at__lt = timezone.now()
    ).delete()
    print(f"удалено: {deleted}")