from user.permissions import IsAdminOrModerator, IsAdmin
from django.contrib.auth.models import AnonymousUser
from blog.models import Page, Post, Tag
from rest_framework import permissions
from user.models import User


class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post):
            obj = obj.page
        return obj.owner == request.user


class IsPageNotPrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post):
            obj = obj.page
        if IsPageOwnerOrAdminOrModerator.has_object_permission(self, request, view, obj):
            return True
        return not obj.is_private


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post):
            obj = obj.page
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
