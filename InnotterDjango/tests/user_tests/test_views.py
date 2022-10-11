from rest_framework.permissions import IsAuthenticated
from user.views import UserViewSet
from rest_framework import status
from user.models import User
import pytest


pytestmark = pytest.mark.django_db

block_view = UserViewSet.as_view({'patch': 'block'})
liked_posts_view = UserViewSet.as_view({'get': 'liked_posts'})


class TestUserViewSet:
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

    def test_get_permissions(self):
        self = UserViewSet()
        self.action = 'list'
        self.get_permissions() is IsAuthenticated
