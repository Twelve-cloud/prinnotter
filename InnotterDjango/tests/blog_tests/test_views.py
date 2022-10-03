from blog.views import TagViewSet, PageViewSet, PostViewSet, UserPageFilter
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.permissions import IsAuthenticated
from InnotterDjango.aws_s3_client import S3Client
from blog.models import Page, Post
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db

page_create_view = PageViewSet.as_view({'post': 'create'})
update_view = PageViewSet.as_view({'patch': 'update'})
block_view = PageViewSet.as_view({'patch': 'block'})
follow_view = PageViewSet.as_view({'patch': 'follow'})
requests_view = PageViewSet.as_view({'get': 'requests'})
accept_view = PageViewSet.as_view({'patch': 'accept'})
accept_all_view = PageViewSet.as_view({'patch': 'accept_all'})
decline_view = PageViewSet.as_view({'patch': 'decline'})
decline_all_view = PageViewSet.as_view({'patch': 'decline_all'})
news_view = PageViewSet.as_view({'get': 'news'})

post_create_view = PostViewSet.as_view({'post': 'create'})
list_view = PostViewSet.as_view({'get': 'list'})
like_view = PostViewSet.as_view({'patch': 'like'})

search_view = UserPageFilter.as_view()


class TestTagViewSet:
    def test_get_permissions(self):
        self = TagViewSet()
        self.action = 'list'
        assert isinstance(self.get_permissions()[0], IsAuthenticated) is True


class TestPageViewSet:
    def test_get_permissions(self):
        self = PageViewSet()
        self.action = 'list'
        assert isinstance(self.get_permissions()[0], IsAuthenticated) is True

    def test_create(self, api_factory, admin, mocker, pageperm):
        file = SimpleUploadedFile('file.txt', b'', content_type='text/plain')
        request = api_factory.post('', {'image': file, 'uuid': ''}, format='multipart')
        request.user = admin

        mock = mocker.MagicMock()
        mocker.patch('blog.views.add_image_to_s3_bucket', mock)
        mocker.patch('blog.views.add_url_to_request', mock)
        mocker.patch.object(S3Client, 'create_url', mock)
        response = page_create_view(request)

        assert mock.call_count == 3
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, api_factory, admin, page, mocker, pageperm):
        file = SimpleUploadedFile('file.txt', b'', content_type='text/plain')
        request = api_factory.patch('', {'image': file}, format='multipart')
        request.user = admin

        mock = mocker.MagicMock()
        mocker.patch('blog.views.add_image_to_s3_bucket', mock)
        mocker.patch('blog.views.add_url_to_request', mock)
        mocker.patch.object(S3Client, 'create_url', mock)
        response = update_view(request, **{'pk': page.pk})

        assert mock.call_count == 3
        assert response.status_code == status.HTTP_400_BAD_REQUEST

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
        assert isinstance(self.get_permissions()[0], IsAuthenticated) is True

    def test_get_queryset(self, page, mocker):
        mock = mocker.MagicMock()
        mock.kwargs = {'parent_lookup_page_id': page.id}

        posts = PostViewSet.get_queryset(mock)
        assert len(posts) == 0

        page.post = Post.objects.create(page=page)

        posts = PostViewSet.get_queryset(mock)
        assert len(posts) == 1

    def test_create(self, api_factory, post_json, mocker, postperm):
        request = api_factory.post('', post_json, format='json')

        request.build_absolute_uri = mocker.MagicMock()
        send_notification = mocker.MagicMock()
        mocker.patch('blog.views.send_notification_to_followers', send_notification)
        response = post_create_view(request, parent_lookup_page_id=post_json['page'])

        request.build_absolute_uri.assert_called_once()
        send_notification.assert_called_once()
        response.status_code == status.HTTP_200_OK

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


class TestUserPageFilter:
    def test_search(self, api_factory, user, page):
        request = api_factory.get('/api/v1/blog/search/')
        request.user = user

        response = search_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        request.GET = {'type': 'user', 'username': user.username}
        response = search_view(request)
        assert response.data[0]['username'] == user.username

        request.GET = {'type': 'page', 'name': page.name}
        response = search_view(request)
        assert response.data[0]['name'] == page.name
