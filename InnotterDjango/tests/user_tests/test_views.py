from rest_framework.permissions import IsAuthenticated
from user.serializers import UserSerializer
from user.views import UserViewSet
from rest_framework import status
from user.models import User
import pytest


pytestmark = pytest.mark.django_db

create_view = UserViewSet.as_view({'post': 'create'})
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
        response.status_code == status.HTTP_200_OK

        User.objects.get(email=user_json['email']).delete()

        request = api_factory.post('', user_json, format='json')
        request.build_absolute_uri = mocker.MagicMock()
        send_verification = mocker.MagicMock()
        mocker.patch('user.views.send_verification_link', send_verification)
        request.user = admin
        response = create_view(request)
        assert not request.build_absolute_uri.called
        assert not send_verification.called
        response.status_code == status.HTTP_200_OK

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
