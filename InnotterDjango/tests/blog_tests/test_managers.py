from blog.models import Post
import pytest


pytestmark = pytest.mark.django_db


class TestPostManager:
    def test_get_posts_of_page(self, page):
        assert len(Post.objects.get_posts_of_page(page.id)) == 0
        page.post = Post.objects.create(page=page)
        assert len(Post.objects.get_posts_of_page(page.id)) == 1
