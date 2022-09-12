from user.permissions import (
    IsAdmin, IsModerator, IsAdminOrModerator, IsUserOwner,
    IsUserOwnerOrAdmin, IsNotAuthentificatedOrAdmin
)
from django.contrib.auth.models import AnonymousUser
import pytest


pytestmark = pytest.mark.django_db


class TestUserPermissions:
    def test_is_admin(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsAdmin.has_permission(..., request, ...) is False
        request.user = created_moderator
        assert IsAdmin.has_permission(..., request, ...) is False
        request.user = created_admin
        assert IsAdmin.has_permission(..., request, ...) is True

    def test_is_moderator(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsModerator.has_permission(..., request, ...) is False
        request.user = created_admin
        assert IsModerator.has_permission(..., request, ...) is False
        request.user = created_moderator
        assert IsModerator.has_permission(..., request, ...) is True

    def test_is_admin_or_moderator(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsAdminOrModerator.has_permission(..., request, ...) is False
        request.user = created_admin
        assert IsAdminOrModerator.has_permission(..., request, ...) is True
        request.user = created_moderator
        assert IsAdminOrModerator.has_permission(..., request, ...) is True

    def test_is_user_owner(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user

        obj = AnonymousUser()
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is False
        obj = created_user
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is True

        request.user = created_moderator
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is False
        request.user = created_admin
        assert IsUserOwner.has_object_permission(..., request, ..., obj) is False

    def test_is_user_owner_or_admin(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user

        obj = AnonymousUser()
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is False
        obj = created_user
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is True

        request.user = created_admin
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is True
        request.user = created_moderator
        assert IsUserOwnerOrAdmin.has_object_permission(..., request, ..., obj) is False

    def test_is_not_authntificated_or_admin(self, created_user, created_moderator, created_admin, mocker):
        request = mocker.MagicMock()

        request.user = created_user
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is False
        request.user = created_moderator
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is False
        request.user = created_admin
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is True
        request.user = AnonymousUser()
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request, ...) is True
