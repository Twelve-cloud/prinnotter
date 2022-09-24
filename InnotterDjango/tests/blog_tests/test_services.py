from blog.services import (
    set_blocking, follow_page, like_or_unlike_post,
    add_user_to_followers, add_all_users_to_followers,
    remove_user_from_requests, remove_all_users_from_requests,
    search_pages_by_params
)
from django.http import Http404
import pytest


pytestmark = pytest.mark.django_db


class TestBlogServices:
    def test_set_blocking(self, page):
        assert page.unblock_date is None
        set_blocking(page, '2025-09-26 00:00:00')
        assert page.unblock_date is not None

    def test_follow_page(self, page, user):
        assert user not in page.followers.all()
        follow_page(page, user)
        assert user in page.followers.all()
        follow_page(page, user)
        assert user not in page.followers.all()

        page.is_private = True
        page.save()

        assert user not in page.follow_requests.all()
        follow_page(page, user)
        assert user in page.follow_requests.all()
        follow_page(page, user)
        assert user not in page.follow_requests.all()

    def test_like_or_unlike_post(self, post, user):
        assert user not in post.users_liked.all()
        like_or_unlike_post(post, user)
        assert user in post.users_liked.all()
        like_or_unlike_post(post, user)
        assert user not in post.users_liked.all()

    def test_add_user_to_followers(self, page, user):
        page.follow_requests.add(user.pk)
        assert user in page.follow_requests.all()

        add_user_to_followers(page, user.id)

        assert user not in page.follow_requests.all()
        assert user in page.followers.all()

        with pytest.raises(Http404):
            add_user_to_followers(page, user_id=999)

    def test_add_all_users_to_followers(self, page, users):
        for user in users:
            page.follow_requests.add(user.pk)

        assert len(page.follow_requests.all()) == len(users)

        add_all_users_to_followers(page)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == len(users)

    def test_remove_user_from_requests(self, page, user):
        page.follow_requests.add(user.pk)
        assert user in page.follow_requests.all()

        remove_user_from_requests(page, user.id)

        assert user not in page.follow_requests.all()
        assert user not in page.followers.all()

        with pytest.raises(Http404):
            remove_user_from_requests(page, user_id=999)

    def test_remove_all_users_from_request(self, page, users):
        for user in users:
            page.follow_requests.add(user.pk)

        assert len(page.follow_requests.all()) == len(users)

        remove_all_users_from_requests(page)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == 0

    def test_search_pages_by_params(self, page):
        pages = search_pages_by_params(name=page.name)
        assert page in pages
