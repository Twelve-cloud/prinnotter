from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'u', 'User'
        MODERATOR = 'm', 'Moderator'
        ADMIN = 'a', 'Admin'
        __empty__ = 'Choose rolename'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )

    image_s3_path = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='PathToImage',
    )

    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        verbose_name='Rolename',
    )

    is_blocked = models.BooleanField(
        default=False,
        verbose_name='Blocked?',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-is_blocked', 'username']
        db_table = 'User'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/users/{self.pk}/'
