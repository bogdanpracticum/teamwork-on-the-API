from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_CHOICES = (
    ('5', 'Отлично'),
    ('4', 'Хорошо'),
    ('3', 'Нормально'),
    ('2', 'Плохо'),
    ('1', 'Ужасно'),
)


class Title(models.Model):
    pass


class Review(models.Model):
    """Модель отзывов на произведения."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата создания', auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        'Дата изменения', auto_now_add=True, db_index=True)
    rating_choices = DEFAULT_CHOICES
    mark = models.CharField(
        max_length=20,
        verbose_name=('Value'),
        choices=rating_choices,
    )


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата создания', auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        'Дата изменения', auto_now_add=True, db_index=True)
