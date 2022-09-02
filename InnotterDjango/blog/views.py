from blog.permissions import (
    IsPageNotPrivate, IsPageNotBlocked, IsPageOwner,
    IsPageOwnerOrAdmin, IsPageOwnerOrAdminOrModerator
)
from blog.serializers import TagSerializer, PageSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdminOrModerator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from blog.models import Tag, Page, Post
from rest_framework import status


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
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
        'follow': (
            IsAuthenticated,
            IsPageNotBlocked
        ),
        'requests': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked
        ),
        'accept_all': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked
        ),
        'decline_all': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked
        ),
        'accept': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked
        ),
        'decline': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    @action(detail=True, methods=['patch'])
    def block(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        page.unblock_date = request.data.get('unblock_date', False)
        page.save()

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def follow(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if page.owner == request.user:
            return Response('You can not follow on your own page', status=status.HTTP_400_BAD_REQUEST)

        if page.is_private:
            if request.user in page.follow_requests.all():
                page.follow_requests.remove(request.user.pk)
            else:
                page.follow_requests.add(request.user.pk)
        else:
            if request.user in page.followers.all():
                page.followers.remove(request.user.pk)
            else:
                page.followers.add(request.user.pk)

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response('Page is not private', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(page)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def accept_all(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response('Page is not private', status=status.HTTP_400_BAD_REQUEST)

        # logic

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def decline_all(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response('Page is not private', status=status.HTTP_400_BAD_REQUEST)

        # logic

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response('Page is not private', status=status.HTTP_400_BAD_REQUEST)

        # logic

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def decline(self, request, pk=None):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return Response('Page is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response('Page is not private', status=status.HTTP_400_BAD_REQUEST)

        # logic

        return Response('Success', status=status.HTTP_200_OK)


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
        'like': (
            IsAuthenticated,
            IsPageNotPrivate,
            IsPageNotBlocked
        ),
    }

    def get_queryset(self):
        parent_page_id = self.kwargs.get('parent_lookup_page_id')
        return Post.objects.get_posts_of_page(parent_page_id)

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    @action(detail=True, methods=['patch'])
    def like(self, request, parent_lookup_page_id=None, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response('Post is not found', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)

        if request.user in post.liked_posts.all():
            post.liked_posts.remove(request.user.pk)
        else:
            post.liked_posts.add(request.user.pk)

        return Response('Success', status=status.HTTP_200_OK)
