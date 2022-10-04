from django.db import models
from django.conf import settings

from .validators import validate_year


class CaGeAbstractModel(models.Model):
    """Абстрактная модель для Категорий и жанров."""
    name = models.CharField('Название', max_length=settings.NAME_SIZE)
    slug = models.SlugField('Слаг', unique=True, max_length=settings.SLUG_SIZE)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Category(CaGeAbstractModel):
    """Модель категорий."""

    class Meta(CaGeAbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CaGeAbstractModel):
    """Модель жанров."""

    class Meta(CaGeAbstractModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def name_list(self):
        return (self.name, self.slug)


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField('Название', max_length=settings.NAME_SIZE)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        blank=True,
        null=True,
        db_index=True,
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
        max_length=settings.NAME_SIZE
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]
