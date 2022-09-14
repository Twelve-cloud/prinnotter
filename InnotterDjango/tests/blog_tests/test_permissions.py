from blog.permissions import (
    IsPageOwner, IsNotPageOwner, IsPageOwnerOrAdmin,
    IsPageOwnerOrAdminOrModerator, IsPagePrivate,
    IsPageNotPrivate, IsPageNotBlocked
)
from blog.models import Page
import pytest


pytestmark = pytest.mark.django_db


class TestBlogPermissions:
    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_owner(self, request, _request, obj, anon, moder, admin):
        obj = request.getfixturevalue(obj)

        _request.user = obj.owner if isinstance(obj, Page) else obj.page.owner
        assert IsPageOwner.has_object_permission(..., _request, ..., obj) is True
        _request.user = anon
        assert IsPageOwner.has_object_permission(..., _request, ..., obj) is False
        _request.user = moder
        assert IsPageOwner.has_object_permission(..., _request, ..., obj) is False
        _request.user = admin
        assert IsPageOwner.has_object_permission(..., _request, ..., obj) is False

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_not_page_owner(self, request, _request, obj, anon, moder, admin):
        obj = request.getfixturevalue(obj)

        _request.user = obj.owner if isinstance(obj, Page) else obj.page.owner
        assert IsNotPageOwner.has_object_permission(..., _request, ..., obj) is False
        _request.user = anon
        assert IsNotPageOwner.has_object_permission(..., _request, ..., obj) is True
        _request.user = moder
        assert IsNotPageOwner.has_object_permission(..., _request, ..., obj) is True
        _request.user = admin
        assert IsNotPageOwner.has_object_permission(..., _request, ..., obj) is True

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_owner_or_admin(self, request, _request, obj, anon, moder, admin):
        obj = request.getfixturevalue(obj)

        _request.user = obj.owner if isinstance(obj, Page) else obj.page.owner
        assert IsPageOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is True
        _request.user = anon
        assert IsPageOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is False
        _request.user = moder
        assert IsPageOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is False
        _request.user = admin
        assert IsPageOwnerOrAdmin.has_object_permission(..., _request, ..., obj) is True

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_owner_or_admin_or_moderator(self, request, _request, obj, anon, moder, admin):
        obj = request.getfixturevalue(obj)

        _request.user = obj.owner if isinstance(obj, Page) else obj.page.owner
        assert IsPageOwnerOrAdminOrModerator.has_object_permission(..., _request, ..., obj) is True
        _request.user = anon
        assert IsPageOwnerOrAdminOrModerator.has_object_permission(..., _request, ..., obj) is False
        _request.user = moder
        assert IsPageOwnerOrAdminOrModerator.has_object_permission(..., _request, ..., obj) is True
        _request.user = admin
        assert IsPageOwnerOrAdminOrModerator.has_object_permission(..., _request, ..., obj) is True

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_private(self, request, _request, obj):
        obj = request.getfixturevalue(obj)

        assert IsPagePrivate.has_object_permission(..., _request, ..., obj) is False

        if isinstance(obj, Page):
            obj.is_private = True
        else:
            obj.page.is_private = True

        assert IsPagePrivate.has_object_permission(..., _request, ..., obj) is True

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_not_private(self, request, _request, obj, anon, user):
        obj = request.getfixturevalue(obj)

        _request.user = anon
        assert IsPageNotPrivate.has_object_permission(..., _request, ..., obj) is True
        _request.user = user
        assert IsPageNotPrivate.has_object_permission(..., _request, ..., obj) is True

        if isinstance(obj, Page):
            obj.is_private = True
        else:
            obj.page.is_private = True

        _request.user = anon
        assert IsPageNotPrivate.has_object_permission(..., _request, ..., obj) is False
        _request.user = user
        assert IsPageNotPrivate.has_object_permission(..., _request, ..., obj) is True

    @pytest.mark.parametrize('obj', ['page', 'post'])
    def test_is_page_not_blocked(self, request, _request, obj, anon, admin):
        obj = request.getfixturevalue(obj)

        _request.user = anon
        assert IsPageNotBlocked.has_object_permission(..., _request, ..., obj) is True
        _request.user = admin

        assert IsPageNotBlocked.has_object_permission(..., _request, ..., obj) is True
        if isinstance(obj, Page):
            obj.unblock_date = '2025-09-26 00:00:00'
        else:
            obj.page.unblock_date = '2025-09-26 00:00:00'

        _request.user = anon
        assert IsPageNotBlocked.has_object_permission(..., _request, ..., obj) is False
        _request.user = admin
        assert IsPageNotBlocked.has_object_permission(..., _request, ..., obj) is True
