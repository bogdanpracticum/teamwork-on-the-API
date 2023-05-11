from django.db import models


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


class Titles(models.Model):
    '''модель произведений искусства'''
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    desription = models.TextField()

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


class TitlesGenres(models.Model):
    '''Промежуточная модель для связи ManyToMany'''
    title = models.ForeignKey(
        Titles,
        on_delete=models.SET_NULL,
        related_name='titlesgenres',
        null=True
    )