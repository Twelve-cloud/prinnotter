from user.permissions import (
    IsAdmin, IsModerator, IsAdminOrModerator, IsUserOwner,
    IsUserOwnerOrAdmin, IsNotAuthentificatedOrAdmin
)
from django.contrib.auth.models import AnonymousUser
import pytest


pytestmark = pytest.mark.django_db


class TestUserPermissions:
    def test_is_admin(self, user, moderator, admin, request_):
        request_.user = user
        assert IsAdmin.has_permission(..., request_, ...) is False
        request_.user = moderator
        assert IsAdmin.has_permission(..., request_, ...) is False
        request_.user = admin
        assert IsAdmin.has_permission(..., request_, ...) is True

    def test_is_moderator(self, user, moderator, admin, request_):
        request_.user = user
        assert IsModerator.has_permission(..., request_, ...) is False
        request_.user = admin
        assert IsModerator.has_permission(..., request_, ...) is False
        request_.user = moderator
        assert IsModerator.has_permission(..., request_, ...) is True

    def test_is_admin_or_moderator(self, user, moderator, admin, request_):
        request_.user = user
        assert IsAdminOrModerator.has_permission(..., request_, ...) is False
        request_.user = admin
        assert IsAdminOrModerator.has_permission(..., request_, ...) is True
        request_.user = moderator
        assert IsAdminOrModerator.has_permission(..., request_, ...) is True

    def test_is_user_owner(self, user, moderator, admin, request_):
        request_.user = user
        obj = AnonymousUser()
        assert IsUserOwner.has_object_permission(..., request_, ..., obj) is False
        obj = user
        assert IsUserOwner.has_object_permission(..., request_, ..., obj) is True
        request_.user = admin
        assert IsUserOwner.has_object_permission(..., request_, ..., obj) is False
        request_.user = moderator
        assert IsUserOwner.has_object_permission(..., request_, ..., obj) is False

    def test_is_user_owner_or_admin(self, user, moderator, admin, request_):
        request_.user = user
        obj = AnonymousUser()
        assert IsUserOwnerOrAdmin.has_object_permission(..., request_, ..., obj) is False
        obj = user
        assert IsUserOwnerOrAdmin.has_object_permission(..., request_, ..., obj) is True
        request_.user = admin
        assert IsUserOwnerOrAdmin.has_object_permission(..., request_, ..., obj) is True
        request_.user = moderator
        assert IsUserOwnerOrAdmin.has_object_permission(..., request_, ..., obj) is False

    def test_is_not_authentificated_or_admin(self, user, moderator, admin, request_):
        request_.user = user
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request_, ...) is False
        request_.user = moderator
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request_, ...) is False
        request_.user = admin
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request_, ...) is True
        request_.user = AnonymousUser()
        assert IsNotAuthentificatedOrAdmin.has_permission(..., request_, ...) is True
