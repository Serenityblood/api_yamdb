from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    password = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=150, default='user', blank=False)
    bio = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.username
