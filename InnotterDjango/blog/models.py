from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Name',
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'Tag'

    def __str__(self):
        return f'{self.id}. {self.name}'

    def get_absolute_url(self):
        return f'/tags/{self.pk}/'


class Page(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Name',
    )

    uuid = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='UUID',
    )

    description = models.TextField(
        verbose_name='Description',
    )

    tags = models.ManyToManyField(
        'blog.Tag',
        related_name='pages',
        verbose_name='Tags',
    )

    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='pages',
        verbose_name='Owner',
    )

    followers = models.ManyToManyField(
        'user.User',
        related_name='follows',
        verbose_name='Followers',
    )

    image = models.URLField(
        null=True,
        blank=True,
        verbose_name='Image',
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name='Private?',
    )

    follow_requests = models.ManyToManyField(
        'user.User',
        related_name='requests',
        verbose_name='Requests',
    )

    unblock_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Unblock date',
    )

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['uuid']
        db_table = 'Page'

    def __str__(self):
        return f'{self.id}. {self.name}'

    def get_absolute_url(self):
        return f'/pages/{self.pk}/'


class Post(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Page',
    )

    content = models.CharField(
        max_length=180,
        verbose_name='Content',
    )

    liked_posts = models.ManyToManyField(
        'user.User',
        related_name='liked_posts',
        verbose_name='Liked posts',
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        related_name='replies',
        verbose_name='Reply to',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        db_table = 'Post'

    def __str__(self):
        return f'id: {self.pk}, page: {self.page.name}'

    def get_absolute_url(self):
        return f'/posts/{self.pk}/'
