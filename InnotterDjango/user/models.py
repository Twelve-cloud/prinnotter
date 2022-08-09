from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from datetime import datetime, timedelta
import jwt


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, role='u'):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password, role='a')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        USER = 'u', 'User'
        MODERATOR = 'm', 'Moderator'
        ADMIN = 'a', 'Admin'
        __empty__ = 'Choose rolename'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        db_column='Email'
    )

    username = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Username',
        db_column='Username'
    )

    image_s3_path = models.CharField(
        max_length=200,
        null=True,
        blank=True,
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

    def generate_access_token(self):
        dt = datetime.now() + timedelta(minutes=1)
        payload = {'id': self.pk, 'exp': int(dt.strftime('%s'))}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def generate_refresh_token(self):
        dt = datetime.now() + timedelta(minutes=2)
        payload = {'id': self.pk, 'exp': int(dt.strftime('%s'))}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
