from django.db import models


class PostManager(models.Manager):
    def get_posts_of_page(self, page_id):
        return self.filter(page=page_id)
