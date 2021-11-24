from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from djoser.serializers import User


class UserAdditionalSerializer(serializers.ModelSerializer):
    """
    Дополнительная информация о пользователе
    """
    subscribers_quantity = serializers.SerializerMethodField()
    subscriptions_quantity = serializers.SerializerMethodField()

    class Meta:
        model = User

    def get_subscriptions_quantity(self,obj):
        """
        Получить количество подписок
        """
        return obj.subscriptions.count()

    def get_subscribers_quantity(self,obj):
        """
        Получить количество подписчиков
        """
        return obj.subscribers.count()


class UserSerializer(serializers.ModelSerializer):
    """
    Пользователь (сериализатор)
    """
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','gender','avatar']

        read_only_fields = ['id','email']


class UserDetailsSerializer(UserAdditionalSerializer,UserSerializer):
    """
    Детали пользователя (сериализатор)
    """
    class Meta:
        model = User
        exclude = ['password','subscriptions']
        read_only_fields = ['email','last_login','date_joined','updated_at']


class CurrentUserDetailsSerializer(UserDetailsSerializer):
    """
    Детали текущего пользователя (сериализатор)
    """

    def update(self, instance, validated_data):
        """
        Обновление пользователя
        """
        if instance.is_superuser or instance.is_staff:
            instance.is_active = validated_data.get('is_active', instance.is_active)

        if instance.is_superuser:
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.is_staff = validated_data.get('is_staff', instance.is_staff)
            try:
                instance.user_permissions.set(validated_data.get('user_permissions', instance.user_permissions))
            except TypeError:
                instance.tags.set(Permission.objects.none())
            try:
                instance.groups.set(validated_data.get('groups', instance.groups))
            except TypeError:
                instance.tags.set(Group.objects.none())

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.gender = validated_data.get('gender', instance.gender)

        instance.save()
        return instance
