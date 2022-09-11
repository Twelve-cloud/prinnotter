from user.permissions import (
    IsAdmin, IsModerator, IsAdminOrModerator, IsUserOwner,
    IsUserOwnerOrAdmin, IsNotAuthentificatedOrAdmin
)
from django.contrib.auth.models import AnonymousUser
from user.models import User
from model_bakery import baker
import pytest


pytestmark = pytest.mark.django_db


class TestPermissions:
    def test_is_admin(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsAdmin.has_permission(..., request, ...) is False
        request.user.role = 'm'
        assert IsAdmin.has_permission(..., request, ...) is False
        request.user.role = 'a'
        assert IsAdmin.has_permission(..., request, ...) is True

    def test_is_moderator(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsModerator.has_permission(..., request, ...) is False
        request.user.role = 'a'
        assert IsModerator.has_permission(..., request, ...) is False
        request.user.role = 'm'
        assert IsModerator.has_permission(..., request, ...) is True

    def test_is_admin_or_moderator(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsAdminOrModerator.has_permission(..., request, ...) is False
        request.user.role = 'a'
        assert IsAdminOrModerator.has_permission(..., request, ...) is True
        request.user.role = 'm'
        assert IsAdminOrModerator.has_permission(..., request, ...) is True

    def test_is_user_owner(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user

        obj = AnonymousUser()
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is False
        obj = baker.make(User, role='m')
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is False
        obj = created_user
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is True

    def test_is_user_owner_or_admin(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user

        obj = AnonymousUser()
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is False
        obj = created_user
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is True
        request.user = baker.make(User, role='a')
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is True

    def test_is_not_authntificated_or_admin(self, created_user, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is False
        request.user.role = 'm'
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is False
        request.user.role = 'a'
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is True
        request.user = AnonymousUser()
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is True
