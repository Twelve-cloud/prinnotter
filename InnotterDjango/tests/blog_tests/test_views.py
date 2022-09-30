from blog.views import TagViewSet, PageViewSet, PostViewSet, search
from rest_framework.permissions import IsAuthenticated
from blog.models import Page, Post
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db

block_view = PageViewSet.as_view({'patch': 'block'})
follow_view = PageViewSet.as_view({'patch': 'follow'})
requests_view = PageViewSet.as_view({'get': 'requests'})
accept_view = PageViewSet.as_view({'patch': 'accept'})
accept_all_view = PageViewSet.as_view({'patch': 'accept_all'})
decline_view = PageViewSet.as_view({'patch': 'decline'})
decline_all_view = PageViewSet.as_view({'patch': 'decline_all'})
news_view = PageViewSet.as_view({'get': 'news'})

list_view = PostViewSet.as_view({'get': 'list'})
like_view = PostViewSet.as_view({'patch': 'like'})


class TestTagViewSet:
    def test_get_permissions(self):
        self = TagViewSet()
        self.action = 'list'
        self.get_permissions() is IsAuthenticated


class TestPageViewSet:
    def test_get_permissions(self):
        self = PageViewSet()
        self.action = 'list'
        self.get_permissions() is IsAuthenticated

    def test_block(self, api_factory, page, block_json, pageperm):
        request = api_factory.patch('', block_json, format='json')
        response = block_view(request, pk=page.pk)

        page = Page.objects.get(pk=page.pk)

        assert page.unblock_date is not None
        assert response.status_code == status.HTTP_200_OK

    def test_follow(self, api_factory, page, user, pageperm):
        request = api_factory.patch('', '', format='json')
        request.user = user

        assert len(page.followers.all()) == 0

        response = follow_view(request, pk=page.pk)

        assert len(page.followers.all()) == 1
        assert response.status_code == status.HTTP_200_OK

    def test_requests(self, api_factory, page, pageperm):
        request = api_factory.get('')
        response = requests_view(request, pk=page.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_accept(self, api_factory, page, user_json, pageperm):
        request = api_factory.patch('', user_json, format='json')
        page.follow_requests.add(user_json['user_id'])

        assert len(page.follow_requests.all()) == 1

        response = accept_view(request, pk=page.pk)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == 1
        assert response.status_code == status.HTTP_200_OK

    def test_accept_all(self, api_factory, page, users, pageperm):
        request = api_factory.patch('', '', format='json')
        for user in users:
            page.follow_requests.add(user.id)

        assert len(page.follow_requests.all()) == len(users)

        response = accept_all_view(request, pk=page.pk)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == len(users)
        assert response.status_code == status.HTTP_200_OK

    def test_decline(self, api_factory, page, user_json, pageperm):
        request = api_factory.patch('', user_json, format='json')
        page.follow_requests.add(user_json['user_id'])

        assert len(page.follow_requests.all()) == 1

        response = decline_view(request, pk=page.pk)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == 0
        assert response.status_code == status.HTTP_200_OK

    def test_decline_all(self, api_factory, page, users, pageperm):
        request = api_factory.patch('', '', format='json')
        for user in users:
            page.follow_requests.add(user.id)

        assert len(page.follow_requests.all()) == len(users)

        response = decline_all_view(request, pk=page.pk)

        assert len(page.follow_requests.all()) == 0
        assert len(page.followers.all()) == 0
        assert response.status_code == status.HTTP_200_OK

    def test_news(self, api_factory, user, moder, page, post):
        request = api_factory.get('/api/v1/blog/pages/news/')

        request.user = user
        user.pages.add(page)
        response = news_view(request)
        assert response.data[0]['id'] == post.id

        request.user = moder
        moder.follows.add(page)
        response = news_view(request)
        assert response.data[0]['id'] == post.id


class TestPostViewSet:
    def test_get_permissions(self):
        self = PostViewSet()
        self.action = 'list'
        self.get_permissions() is IsAuthenticated

    def test_get_queryset(self, page, mocker):
        mock = mocker.MagicMock()
        mock.kwargs = {'parent_lookup_page_id': page.id}

        posts = PostViewSet.get_queryset(mock)
        assert len(posts) == 0

        page.post = Post.objects.create(page=page)

        posts = PostViewSet.get_queryset(mock)
        assert len(posts) == 1

    def test_list(self, api_factory, page, mocker, postperm):
        mock = mocker.MagicMock()
        mock.kwargs = {'parent_lookup_page_id': page.id}

        request = api_factory.get('')
        response = list_view(request, parent_lookup_page_id=page.id)

        assert response.status_code == status.HTTP_200_OK

    def test_like(self, api_factory, user, page, post, postperm):
        request = api_factory.patch('', '', format='json')
        request.user = user

        assert len(post.users_liked.all()) == 0
        response = like_view(request, parent_lookup_page_id=page.id, pk=post.pk)

        assert len(post.users_liked.all()) == 1
        assert response.status_code == status.HTTP_200_OK


class TestSearch:
    def test_search(self, api_factory, user, page):
        request = api_factory.get('/api/v1/blog/search/')
        request.user = user

        response = search(request)
        assert response.data == 'GET params are not valid'

        request.GET = {'type': 'user', 'username': user.username}
        response = search(request)
        assert response.data[0]['username'] == user.username

        request.GET = {'type': 'page', 'name': page.name}
        response = search(request)
        assert response.data[0]['name'] == page.name
