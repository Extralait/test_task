from decimal import Decimal

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe
from model_utils import FieldTracker
from django.core.validators import MaxValueValidator, MinValueValidator

from api.utils.calculating_distance import calculate_distance


class UserManager(BaseUserManager):
    """
    Менеджер пользователя (Модель)
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        База создания пользователя
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание пользователя
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создание суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Custom User Class
class User(AbstractUser):
    """
    Пользователь (Модель)
    """

    class Gender(models.TextChoices):
        """
        Пол
        """
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    username = None
    email = models.EmailField('Email', unique=True)
    gender = models.CharField('Gender', max_length=20, choices=Gender.choices)
    avatar = models.ImageField(upload_to='avatar', verbose_name='avatar', null=True, blank=True)

    subscriptions = models.ManyToManyField('self', related_name='subscribers', verbose_name='Subscriptions',
                                           symmetrical=False, through='UserSubscription')
    distances = models.ManyToManyField('self', related_name='distance', verbose_name='Subscriptions',
                                           symmetrical=True, through='Distance')

    longitude = models.DecimalField('Longitude',max_digits=9, decimal_places=6, default=Decimal('0'),
                                    validators=[
                                        MaxValueValidator(180),
                                        MinValueValidator(-180)
                                    ])
    latitude = models.DecimalField('Latitude',max_digits=9, decimal_places=6, default=Decimal('0'),
                                   validators=[
                                       MaxValueValidator(90),
                                       MinValueValidator(-90)
                                   ])

    updated_at = models.DateTimeField(auto_now=True)

    tracker = FieldTracker(fields=['longitude', 'latitude'])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'avatar']
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        indexes = [
            models.Index(fields=['longitude', 'latitude']),
        ]

    def avatar_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.avatar)

    avatar_tag.short_description = 'Avatar'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)


class UserSubscription(models.Model):
    """
    Подписки на пользователей
    """
    subscriber = models.ForeignKey(User, related_name="subscriber", verbose_name="Subscriber",
                                   on_delete=models.CASCADE)
    subscribe = models.ForeignKey(User, related_name="subscribe", verbose_name="Subscribe",
                                  on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User subscription'
        verbose_name_plural = 'Users subscription'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'subscribe'], name='unique_user_subscriber')
        ]


class Distance(models.Model):
    """
    Расстояние между пользователями
    """
    pk_pair = models.CharField('PK pair',unique=True, default='1&2', blank=True, max_length=256, primary_key=True)
    user_1 = models.ForeignKey(User, related_name="user_1", verbose_name="User 1",
                               on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="user_2", verbose_name="User 2",
                               on_delete=models.CASCADE)
    user_1_longitude = models.DecimalField('User 1 longitude',max_digits=9, decimal_places=6, default=Decimal('0'))
    user_1_latitude = models.DecimalField('User 1 latitude',max_digits=9, decimal_places=6, default=Decimal('0'))
    user_2_longitude = models.DecimalField('User 2 longitude',max_digits=9, decimal_places=6, default=Decimal('0'))
    user_2_latitude = models.DecimalField('User 1 latitude',max_digits=9, decimal_places=6, default=Decimal('0'))
    distance = models.DecimalField('Distance',max_digits=11, decimal_places=6, default=Decimal('0'))

    class Meta:
        verbose_name = 'Distance'
        verbose_name_plural = 'Distances'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.pk_pair = (f'{min([self.user_1.pk,self.user_2.pk])}&'
                        f'{max([self.user_1.pk,self.user_2.pk])}')
        self.distance = calculate_distance(self.user_1_longitude,
                                           self.user_1_latitude,
                                           self.user_2_longitude,
                                           self.user_2_latitude)
        print(self.distance)
        super().save(*args, **kwargs)
