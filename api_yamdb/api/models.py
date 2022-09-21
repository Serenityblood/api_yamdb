from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    email = models.EmailField('Почта пользователя', unique=True)
    bio = models.TextField(
        'О себе',
        blank=True,
        max_length=300
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=USER_ROLE,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=50, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
        db_index=True,
        #validators=[]
    )
    description = models.TextField(
        max_length=400,
        null=True,
        blank=True,
        verbose_name='Описание'
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
        ordering = ('year',)
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='revievs'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text
