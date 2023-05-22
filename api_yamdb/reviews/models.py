from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_year


class CatGenAbsract(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class Categories(CatGenAbsract):
    '''модель категорий'''

    class Meta(CatGenAbsract.Meta):
        verbose_name = "Категория:",
        verbose_name_plural = "Категории:"


class Genres(CatGenAbsract):
    '''модель жанров'''

    class Meta(CatGenAbsract.Meta):
        verbose_name = "Жанр:",
        verbose_name_plural = "Жанры:"


class Title(models.Model):
    '''модель произведений искусства'''
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(blank=True,
                                       validators=(validate_year,))
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genres,
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
