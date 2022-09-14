from user.permissions import (
    IsAdmin, IsModerator, IsAdminOrModerator, IsUserOwner,
    IsUserOwnerOrAdmin, IsNotAuthentificatedOrAdmin
)
import pytest


pytestmark = pytest.mark.django_db


class TestUserPermissions:
    def test_is_admin(self, _request, anon, user, moder, admin):
        _request.user = anon
        assert IsAdmin.has_permission(..., _request, ...) is False
        _request.user = user
        assert IsAdmin.has_permission(..., _request, ...) is False
        _request.user = moder
        assert IsAdmin.has_permission(..., _request, ...) is False
        _request.user = admin
        assert IsAdmin.has_permission(..., _request, ...) is True

    def test_is_moderator(self, _request, anon, user, moder, admin):
        _request.user = anon
        assert IsModerator.has_permission(..., _request, ...) is False
        _request.user = user
        assert IsModerator.has_permission(..., _request, ...) is False
        _request.user = moder
        assert IsModerator.has_permission(..., _request, ...) is True
        _request.user = admin
        assert IsModerator.has_permission(..., _request, ...) is False

    def test_is_admin_or_moderator(self, _request, anon, user, moder, admin):
        _request.user = anon
        assert IsAdminOrModerator.has_permission(..., _request, ...) is False
        _request.user = user
        assert IsAdminOrModerator.has_permission(..., _request, ...) is False
        _request.user = moder
        assert IsAdminOrModerator.has_permission(..., _request, ...) is True
        _request.user = admin
        assert IsAdminOrModerator.has_permission(..., _request, ...) is True

    def test_is_not_authentificated_or_admin(self, _request, anon, user, moder, admin):
        _request.user = anon
        assert IsNotAuthentificatedOrAdmin.has_permission(..., _request, ...) is True
        _request.user = user
        assert IsNotAuthentificatedOrAdmin.has_permission(..., _request, ...) is False
        _request.user = moder
        assert IsNotAuthentificatedOrAdmin.has_permission(..., _request, ...) is False
        _request.user = admin
        assert IsNotAuthentificatedOrAdmin.has_permission(..., _request, ...) is True

    @pytest.mark.parametrize('obj', ['user', 'moder', 'admin'])
    def test_is_user_owner(self, request, _request, obj, anon):
        obj = request.getfixturevalue(obj)
        _request.user = obj
        assert IsUserOwner.has_object_permission(..., _request, ..., obj) is True
        _request.user = anon
        assert IsUserOwner.has_object_permission(..., _request, ..., obj) is False

    @pytest.mark.parametrize('obj', ['user', 'moder', 'admin'])
    def test_is_user_owner_or_admin(self, request, _request, obj, anon, admin):
        obj = request.getfixturevalue(obj)
        _request.user = obj
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is True
        _request.user = anon
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is False
        _request.user = admin
        assert IsUserOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is True
