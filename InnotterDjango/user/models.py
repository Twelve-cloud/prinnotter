from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime, timedelta
from user.managers import UserManager
import jwt


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        USER = 'u', 'User'
        MODERATOR = 'm', 'Moderator'
        ADMIN = 'a', 'Admin'
        __empty__ = 'Choose rolename'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )

    username = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Username',
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
    REQUIRED_FIELDS = ['username', 'password']
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-is_blocked', 'username']
        db_table = 'User'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/user/users/{self.pk}/'

    def generate_token(self, *, type):
        lifetime = timedelta(minutes=15) if type == 'access' else timedelta(days=30)
        dt = datetime.now() + lifetime
        payload = {'id': self.pk, 'exp': int(dt.strftime('%s'))}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
