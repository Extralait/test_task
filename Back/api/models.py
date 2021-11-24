from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe


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

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','gender','avatar']
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

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
