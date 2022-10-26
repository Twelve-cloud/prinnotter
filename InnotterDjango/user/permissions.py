from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
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


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsAdmin.has_permission(self, request, view) or \
            IsModerator.has_permission(self, request, view)


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            return False
        return obj == request.user


class IsUserOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdmin.has_permission(self, request, view) or \
            IsUserOwner.has_object_permission(self, request, view, obj)


class IsNotAuthentificatedOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not IsAuthenticated.has_permission(self, request, view) or \
            IsAdmin.has_permission(self, request, view)
