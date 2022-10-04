from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import CustomUser


class ReCoAbstractModel(models.Model):
    """Абстрактная модель для ревью и комментариев."""
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateField(
        'Дата публикации',
        auto_now_add=True
    )
    text = models.TextField('Текст комментария')

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:settings.TEXT_SIZE]


class Review(ReCoAbstractModel):
    """Модель ревью."""
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, message=('Не может быть меньше 1')),
            MaxValueValidator(10, message=('Не может быть больше 10'))
        ],
        default=1
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta(ReCoAbstractModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]
        default_related_name = 'reviews'


class Comment(ReCoAbstractModel):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(ReCoAbstractModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
