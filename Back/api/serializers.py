from rest_framework import serializers
from djoser.serializers import User


# class CurrentUserSerializer(serializers.ModelSerializer):
#     """
#     Детали текущего пользователя (сериализатор)
#     """
#     def __init__(self, *args, **kwargs):
#         kwargs['partial'] = True
#         super(CurrentUserSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = User
#         exclude = ['password', 'user_subscriptions',
#                    'drop_subscriptions','owner_key']
#
#         read_only_fields = ['last_login','wallet_number'
#                             'date_joined', 'drops','collections']
#
#     def update(self, instance, validated_data):
#
#         if instance.is_superuser or instance.is_staff:
#             instance.is_active = validated_data.get('is_active', instance.is_active)
#             instance.is_verify = validated_data.get('is_verify', instance.is_verify)
#             instance.verify_status = validated_data.get('verify_status', instance.verify_status)
#
#         if instance.is_superuser:
#             instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
#             instance.is_staff = validated_data.get('is_staff', instance.is_staff)
#             instance.user_permissions.set(validated_data.get('user_permissions', instance.user_permissions))
#             instance.groups.set(validated_data.get('groups', instance.groups))
#
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.avatar = validated_data.get('avatar', instance.avatar)
#         instance.cover = validated_data.get('cover', instance.cover)
#         instance.email_notification = validated_data.get('email_notification', instance.email_notification)
#         instance.description = validated_data.get('description', instance.description)
#         instance.instagram = validated_data.get('instagram', instance.instagram)
#         instance.twitter = validated_data.get('twitter', instance.twitter)
#         instance.discord = validated_data.get('discord', instance.discord)
#         instance.tiktok = validated_data.get('tiktok', instance.tiktok)
#         instance.telegram = validated_data.get('telegram', instance.telegram)
#         instance.profile_type = validated_data.get('profile_type', instance.profile_type)
#
#         instance.save()
#         return instance
