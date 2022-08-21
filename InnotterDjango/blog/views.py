from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from blog.serializers import TagSerializer, PageSerializer, PostSerializer
from blog.models import Tag, Page, Post
from blog.permissions import (
    IsPageOwner, IsPageNotPrivate, IsPageNotBlocked,
    IsPageOwnerOrAdmin, IsPageOwnerOrAdminOrModerator, IsAdminOrModerator
)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ['get', 'post', 'head', 'delete']
    permission_classes = []
    permission_map = {
        'create': (
            IsAuthenticated,
            IsAdminOrModerator,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'destroy': (
            IsAuthenticated,
            IsAdminOrModerator,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = []
    permission_map = {
        'create': (
            IsAuthenticated,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
            IsPageNotPrivate,
            IsPageNotBlocked,
        ),
        'update': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotPrivate,
            IsPageNotBlocked,
        ),
        'partial_update': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotPrivate,
            IsPageNotBlocked,
        ),
        'destroy': (
            IsAuthenticated,
            IsPageOwnerOrAdmin,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = []
    permission_map = {
        'create': (
            IsAuthenticated,
            IsPageOwner,
        ),
        'list': (
            IsAuthenticated,
            IsPageNotPrivate,
            IsPageNotBlocked,
        ),
        'retrieve': (
            IsAuthenticated,
            IsPageNotPrivate,
            IsPageNotBlocked,
        ),
        'update': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked,
        ),
        'partial_update': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked,
        ),
        'destroy': (
            IsAuthenticated,
            IsPageOwnerOrAdminOrModerator,
            IsPageNotBlocked,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
