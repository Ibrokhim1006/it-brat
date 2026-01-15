from django.db.models.signals import post_save
from django.dispatch import receiver
from resume.models import FavoritesResume, NotificationResume


@receiver(post_save, sender=FavoritesResume)
def create_favorite_notification(sender, instance, created, **kwargs):
    if created:
        # Bildirishnoma yaratish
        notification = NotificationResume.objects.create(favorite=instance)
