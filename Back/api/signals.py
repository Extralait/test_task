from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .utils.image_preprocessing import add_watermark


@receiver(post_save, sender=User)
def post_save_raw_file(sender, instance, created, **kwargs):
    user = User.objects.get(pk = instance.pk)
    if user.avatar:
        user_avatar = user.avatar.file
        add_watermark(user_avatar)