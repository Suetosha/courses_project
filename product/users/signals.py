from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser, Balance


@receiver(post_save, sender=CustomUser)
def post_save_user(sender, instance: CustomUser, created, **kwargs):
    if created:
        balance = Balance.objects.create(user=instance)
        balance.save()
