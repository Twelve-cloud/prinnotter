from user.views import UserViewSet
from rest_framework import status
from user.models import User
import pytest


pytestmark = pytest.mark.django_db

block_view = UserViewSet.as_view({'patch': 'block'})
liked_posts_view = UserViewSet.as_view({'get': 'liked_posts'})


class TestUserViewSet:
    def test_block(self, api_factory, created_user, block_json, mocker):
        check_perm = mocker.MagicMock(return_value=True)
        mocker.patch.object(UserViewSet, 'check_permissions', check_perm)

        request = api_factory.patch('', block_json, format='json')
        response = block_view(request, pk=created_user.pk)

        user = User.objects.get(pk=created_user.pk)

        assert user.is_blocked is True
        assert response.status_code == status.HTTP_200_OK

    def test_liked_posts(self, api_factory, created_user, mocker):
        check_perm = mocker.MagicMock(return_value=True)
        mocker.patch.object(UserViewSet, 'check_permissions', check_perm)
        mocker.patch.object(UserViewSet, 'check_object_permissions', check_perm)

        request = api_factory.get('')
        response = liked_posts_view(request, pk=created_user.pk)

        assert response.status_code == status.HTTP_200_OK
