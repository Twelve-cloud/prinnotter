from blog.permissions import (
    IsPageNotPrivate, IsPageNotBlocked, IsPageOwner,
    IsPageOwnerOrAdmin, IsPageOwnerOrAdminOrModerator
)
from blog.serializers import TagSerializer, PageSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdminOrModerator
from rest_framework.decorators import action
from rest_framework.response import Response
from blog.models import Tag, Page, Post
from rest_framework import viewsets
from rest_framework import status


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
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
    queryset = Page.objects.all()
    serializer_class = PageSerializer
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
            IsPageNotBlocked,
        ),
        'partial_update': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked,
        ),
        'destroy': (
            IsAuthenticated,
            IsPageOwnerOrAdmin,
        ),
        'block': (
            IsAuthenticated,
            IsAdminOrModerator,
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    @action(detail=True, methods=['patch'])
    def block(self, request, pk=None):
        page = Page.objects.get(pk=pk)
        serializer = self.serializer_class(page, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(unblock_date=request.data.get('unblock_date', False))
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
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

    def list(self, request, *args, **kwargs):
        self.queryset = Post.objects.filter(
            page=kwargs.get('parent_lookup_page_id')
        )
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
