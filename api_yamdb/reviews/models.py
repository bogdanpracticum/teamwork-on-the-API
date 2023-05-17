from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_username


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOICES = ((USER, 'Пользователь'), (MODERATOR, 'Модератор'),
                (ADMIN, 'Администратор'))


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
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Немного о себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.role == ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

# Модели Миши


DEFAULT_CHOICES = (
    ('5', 'Отлично'),
    ('4', 'Хорошо'),
    ('3', 'Нормально'),
    ('2', 'Плохо'),
    ('1', 'Ужасно'),
)


class Categories(models.Model):
    '''модель категорий'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория:",
        verbose_name_plural = "Категории:"


class Genres(models.Model):
    '''модель жанров'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр:",
        verbose_name_plural = "Жанры:"


class Title(models.Model):
    '''модель произведений искусства'''
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(blank=True,)
    description = models.TextField(blank=True)

    genre = models.ManyToManyField(
        Genres,
        # on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр:',
        help_text='Выберите жанр:',
        null=True,
        blank=False,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория:',
        help_text='Выберите категорию:',
        null=True,
        blank=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение:",
        verbose_name_plural = "Произведения:"


class Review(models.Model):
    """Модель отзывов на произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Отзыв:",
        verbose_name_plural = "Отзывы:"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_rev_author'
            )
        ]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Комментарий:",
        verbose_name_plural = "Комментарии:"


class TitlesGenres(models.Model):
    '''Промежуточная модель для связи ManyToMany'''
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        related_name='titlesgenres',
        null=True
    )
