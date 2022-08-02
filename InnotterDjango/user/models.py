from django.db import models


class User(AbstractUser):
    """
    User: Represents user account. Contains some necessary fields for every
    user account whether its user or admin. Also contains inner classes for
    determining User rolename and settings of model.
    """
    class Roles(models.TextChoices):
        """
        Roles: Represents User-account role. Contains 4 attributes:
            1. USER with inner value 'u' and outer value 'User'
            2. MODERATOR with inner value 'm' and outer value 'Moderator'
            3. ADMIN with inner value 'a' and outer value 'Admin'
            4. __empty__ with default value 'Choose rolename'
        """
        USER = 'u', 'User'
        MODERATOR = 'm', 'Moderator'
        ADMIN = 'a', 'Admin'
        __empty__ = 'Choose rolename'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        db_column='Email'
    )

    password = models.CharField(
        max_length=32,
        verbose_name='Password',
        db_column='Password'
    )

    image_s3_path = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Avatar path',
        db_column='AvatarPath'
    )

    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        verbose_name='Rolename',
        db_column='Rolename'
    )

    title = models.CharField(
        max_length=80,
        verbose_name='Title',
        db_column='Title'
    )

    is_blocked = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='Blocked?',
        db_column='IsBlocked'
    )

    last_seen = models.DateTimeField(
        verbose_name='Last Seen',
        db_column='LastSeen'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-last_seen', '-is_blocked']
        db_table = 'User'

    def get_absolute_url(self):
        return f'/user/{self.pk}/'

    def __str__(self):
        return self.email
