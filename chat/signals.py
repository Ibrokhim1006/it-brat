from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.middleware import get_current_user
from chat.models import ChatMessage, NotificationChat


@receiver(post_save, sender=ChatMessage)
def create_favorite_notification(sender, instance, created, **kwargs):
    if created:
        # Bildirishnoma yaratish
        notification = NotificationChat.objects.create(favorite=instance)
        print(get_current_user())
