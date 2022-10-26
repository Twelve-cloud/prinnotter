from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.permissions import IsAuthenticated
from InnotterDjango.aws_s3_client import S3Client
from user.serializers import UserSerializer
from user.views import UserViewSet
from rest_framework import status
from user.models import User
import pytest


pytestmark = pytest.mark.django_db

create_view = UserViewSet.as_view({'post': 'create'})
update_view = UserViewSet.as_view({'patch': 'update'})
block_view = UserViewSet.as_view({'patch': 'block'})
liked_posts_view = UserViewSet.as_view({'get': 'liked_posts'})


class TestUserViewSet:
    def test_get_permissions(self):
        user_viewset = UserViewSet()
        user_viewset.action = 'list'
        assert isinstance(user_viewset.get_permissions()[0], IsAuthenticated) is True

    def test_perform_create(self, admin, anon, user_json, mocker):
        user_viewset = UserViewSet()
        serializer = UserSerializer(data=user_json)
        serializer.is_valid(raise_exception=True)
        request = mocker.MagicMock()

        request.user = anon
        serializer.context['request'] = request
        user_viewset.perform_create(serializer)
        assert User.objects.get(email=user_json['email']).is_verified is False

        request.user = admin
        serializer.context['request'] = request
        user_viewset.perform_create(serializer)
        assert User.objects.get(email=user_json['email']).is_verified is True

    def test_create(self, api_factory, user_json, anon, admin, mocker, userperm):
        request = api_factory.post('', user_json, format='json')
        request.build_absolute_uri = mocker.MagicMock()
        send_verification = mocker.MagicMock()
        mocker.patch('user.views.send_verification_link', send_verification)
        request.user = anon
        response = create_view(request)
        request.build_absolute_uri.assert_called_once()
        send_verification.assert_called_once()
        assert response.status_code == status.HTTP_201_CREATED

        User.objects.get(email=user_json['email']).delete()

        request = api_factory.post('', user_json, format='json')
        request.build_absolute_uri = mocker.MagicMock()
        send_verification = mocker.MagicMock()
        mocker.patch('user.views.send_verification_link', send_verification)
        request.user = admin
        response = create_view(request)
        assert not request.build_absolute_uri.called
        assert not send_verification.called
        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, api_factory, admin, mocker, userperm):
        file = SimpleUploadedFile('file.txt', b'', content_type='text/plain')
        request = api_factory.patch('', {'image': file}, format='multipart')
        request.user = admin

        mock = mocker.MagicMock()
        mocker.patch('user.views.add_image_to_s3_bucket', mock)
        mocker.patch('user.views.add_url_to_request', mock)
        mocker.patch.object(S3Client, 'create_url', mock)
        response = update_view(request, **{'pk': request.user.pk})

        assert mock.call_count == 3
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_block(self, api_factory, user, block_json, userperm):
        request = api_factory.patch('', block_json, format='json')
        response = block_view(request, pk=user.pk)
        user = User.objects.get(pk=user.pk)
        assert user.is_blocked is True
        assert response.status_code == status.HTTP_200_OK

    def test_liked_posts(self, api_factory, user, userperm):
        request = api_factory.get('')
        response = liked_posts_view(request, pk=user.pk)
        assert response.status_code == status.HTTP_200_OK
