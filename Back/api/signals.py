from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Distance
from .utils.image_preprocessing import add_watermark


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if instance.avatar:
        user_avatar = instance.avatar.file
        add_watermark(user_avatar)

    if instance.tracker.has_changed('longitude') or instance.tracker.has_changed('latitude'):
        users_coordinates = (User.objects.filter(~Q(pk=instance.pk))
                             .only('pk', 'longitude', 'latitude')
                             .values_list('pk', 'longitude', 'latitude'))
        for user_coordinates in users_coordinates:
            Distance.objects.update_or_create(
                pk_pair=f'{min([instance.pk,user_coordinates[0]])}&'
                        f'{max([instance.pk,user_coordinates[0]])}',
                defaults={'user_1_id': instance.pk,
                          'user_2_id': user_coordinates[0],
                          'user_1_longitude': instance.longitude,
                          'user_1_latitude': instance.latitude,
                          'user_2_longitude': user_coordinates[1],
                          'user_2_latitude': user_coordinates[2]})
