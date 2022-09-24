from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        max_length=300,
        null=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=USER_ROLE,
        default=USER
    )
    is_admin = models.BooleanField(default=False)
    password = models.CharField(
        'Пароль', default='12345', max_length=128, null=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=150,
        null=True
    )
    email = models.EmailField(db_index=True, unique=True)

    REQUIRED_FIELDS = ['email']

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
