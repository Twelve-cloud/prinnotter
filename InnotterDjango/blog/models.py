from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Name',
        db_column='Name'
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'Tag'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tag/{self.pk}/'


class Page(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Name',
        db_column='Name'
    )

    uuid = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='UUID',
        db_column='UUID'
    )

    description = models.TextField(
        verbose_name='Description',
        db_column='Description'
    )

    tags = models.ManyToManyField(
        'blog.Tag',
        related_name='pages',
        verbose_name='Tags',
        db_column='Tags'
    )

    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='pages',
        verbose_name='Owner',
        db_column='Owner'
    )

    followers = models.ManyToManyField(
        'user.User',
        related_name='follows',
        verbose_name='Followers',
        db_column='Followers'
    )

    image = models.URLField(
        null=True,
        blank=True,
        verbose_name='Image',
        db_column='Image'
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name='Private?',
        db_column='IsPrivate'
    )

    follow_requests = models.ManyToManyField(
        'user.User',
        related_name='requests',
        verbose_name='Requests',
        db_column='Requests'
    )

    unblock_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Unblock date',
        db_column='UnblockDate'
    )

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['uuid']
        db_table = 'Page'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/page/{self.pk}/'


class Post(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Page',
        db_column='Page'
    )

    content = models.CharField(
        max_length=180,
        verbose_name='Content',
        db_column='Content'
    )

    likes = models.ManyToManyField(
        'user.User',
        related_name='likes',
        verbose_name='Likes',
        db_column='Likes'
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        related_name='replies',
        verbose_name='Reply to',
        db_column='ReplyTo'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
        db_column='CreatedAt'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
        db_column='UpdatedAt'
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        db_table = 'Post'

    def __str__(self):
        return f'post №{self.pk} on page {self.page.name}'

    def get_absolute_url(self):
        return f'/post/{self.pk}/'
