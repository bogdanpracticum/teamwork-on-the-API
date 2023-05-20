from django.contrib.auth.models import AbstractUser
from django.db import models


from reviews.validators import validate_username


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [(USER, 'Пользователь'), (MODERATOR, 'Модератор'),
                    (ADMIN, 'Администратор')]


class User(AbstractUser):
    username = models.CharField(
        'Никнейм',
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Немного о себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=82,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_staff_status(self):
        if self.role == UserRole.ADMIN or self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = False

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_staff_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRole.USER


class CatGenAbsract(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']
