from blog.permissions import (
    IsPageOwner, IsNotPageOwner, IsPageOwnerOrAdmin,
    IsPageOwnerOrAdminOrModerator, IsPagePrivate,
    IsPageNotPrivate, IsPageNotBlocked
)
from django.contrib.auth.models import AnonymousUser
from blog.models import Page
import pytest


pytestmark = pytest.mark.django_db


# class TestBlogPermissions:
#     @pytest.mark.parametrize('obj', ['page', 'post'])
#     def test_is_page_owner(self, obj, request, request_, moder, admin, anon):
#         obj = request.getfixturevalue(obj)
#         request_.user = obj.owner if isinstance(obj, Page) else obj.page.owner
#         assert IsPageOwner.has_object_permission(..., request_, ..., obj) is True
#         request_.user = moder
#         assert IsPageOwner.has_object_permission(..., request_, ..., obj) is False
#         request_.user = admin
#         assert IsPageOwner.has_object_permission(..., request_, ..., obj) is False
#         request_.user = anon
#         assert IsPageOwner.has_object_permission(..., request_, ..., obj) is False
