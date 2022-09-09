from user.permissions import IsAdminOrModerator, IsAdmin
from rest_framework import permissions
from blog.models import Post


class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post):
            return obj.page.owner == request.user
        return obj.owner == request.user


class IsPageNotPrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsPageOwnerOrAdminOrModerator.has_object_permission(self, request, view, obj):
            return True
        if isinstance(obj, Post):
            return not obj.page.is_private
        return not obj.is_private


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsAdminOrModerator.has_permission(self, request, view):
            return True
        if isinstance(obj, Post):
            return obj.page.unblock_date is None
        return obj.unblock_date is None


class IsPageOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsPageOwner.has_object_permission(self, request, view, obj) or \
            IsAdmin.has_permission(self, request, view)


class IsPageOwnerOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsPageOwner.has_object_permission(self, request, view, obj) or \
            IsAdminOrModerator.has_permission(self, request, view)


class IsNotPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not IsPageOwner.has_object_permission(self, request, view, obj)


class IsPagePrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_private
