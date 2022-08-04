from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
        __empty__ = 'Choose rolename'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        db_column='Email'
    )

    username = models.CharField(
        min_length=8,
        max_length=32,
        unique=True,
        verbose_name='Username',
        db_column='Username'
    )

    image_s3_path = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        editable=False,
        verbose_name='PathToImage',
        db_column='PathToImage'
    )

    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        verbose_name='Rolename',
        db_column='Rolename'
    )

    is_blocked = models.BooleanField(
        default=False,
        verbose_name='Blocked?',
        db_column='Blocked'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-is_blocked', 'username']
        db_table = 'User'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/user/{self.pk}/'
