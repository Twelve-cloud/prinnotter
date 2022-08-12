from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from blog.models import Page, Post, Tag
from user.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == User.Roles.ADMIN


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == User.Roles.MODERATOR


class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        obj = obj.page if isinstance(obj, Post) else obj
        return obj.owner == request.user


class IsPageNotPrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        obj = obj.page if isinstance(obj, Post) else obj
        if IsPageOwnerOrAdminOrModerator.has_object_permission(self, request, view, obj):
            return True
        return not obj.is_private


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        obj = obj.page if isinstance(obj, Post) else obj
        if IsAdminOrModerator.has_permission(self, request, view):
            return True
        return obj.unblock_date is None


class IsPageOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsPageOwner.has_object_permission(self, request, view, obj) or \
            IsAdmin.has_permission(self, request, view)


class IsPageOwnerOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsPageOwner.has_object_permission(self, request, view, obj) or \
            IsAdminOrModerator.has_permission(self, request, view)


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsAdmin.has_permission(self, request, view) or \
            IsModerator.has_permission(self, request, view)
