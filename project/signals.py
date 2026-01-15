from django.db.models.signals import post_save
from django.dispatch import receiver
from project.models import FavoritesProject, Notification


@receiver(post_save, sender=FavoritesProject)
def create_favorite_notification(sender, instance, created, **kwargs):
    if created:
        # Bildirishnoma yaratish
        notification = Notification.objects.create(favorite=instance)