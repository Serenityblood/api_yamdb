from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        max_length=settings.USERNAME_SIZE,
        null=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=USER_ROLE,
        default=USER
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        blank=False,
        max_length=settings.EMAIL_SIZE
    )
    first_name = models.CharField(
        max_length=settings.USERNAME_SIZE, null=False, blank=True
    )
    last_name = models.CharField(
        max_length=settings.USERNAME_SIZE, null=False, blank=True
    )
    username = models.CharField(
        'username',
        max_length=settings.USERNAME_SIZE,
        unique=True,
        validators=[validate_username]
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
