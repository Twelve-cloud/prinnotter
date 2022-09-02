from blog.permissions import (
    IsPageNotPrivate, IsPageNotBlocked, IsPageOwner,
    IsPageOwnerOrAdmin, IsPageOwnerOrAdminOrModerator,
    IsNotPageOwner, IsPagePrivate
)
from blog.services import (
    get_page_by_id, get_post_by_id,
    set_blocking, follow_page,
    like_post
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
            IsPageNotBlocked,
            IsNotPageOwner
        ),
        'requests': (
            IsAuthenticated,
            IsPageOwner,
            IsPageNotBlocked,
            IsPagePrivate
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
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        set_blocking(page, request.data.get('unblock_date', None))
        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def follow(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)
        follow_page(page, request.user)
        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)
        serializer = self.serializer_class(page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response(
                'Page is not private',
                status=status.HTTP_400_BAD_REQUEST
            )

        # logic

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def decline(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response(
                'Page is not private',
                status=status.HTTP_400_BAD_REQUEST
            )

        # logic

        return Response('Success', status=status.HTTP_200_OK)



    @action(detail=True, methods=['patch'])
    def accept_all(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response(
                'Page is not private',
                status=status.HTTP_400_BAD_REQUEST
            )

        # logic

        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def decline_all(self, request, pk=None):
        page = get_page_by_id(pk)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)

        if not page.is_private:
            return Response(
                'Page is not private',
                status=status.HTTP_400_BAD_REQUEST
            )

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

    def list(self, request, *args, **kwargs):
        parent_page_id = self.kwargs.get('parent_lookup_page_id')
        page = get_page_by_id(parent_page_id)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, page)
        return super().list(request, args, kwargs)

    @action(detail=True, methods=['patch'])
    def like(self, request, parent_lookup_page_id=None, pk=None):
        page = get_page_by_id(parent_lookup_page_id)

        if not page:
            return Response(
                'Page is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        post = get_post_by_id(pk)

        if not post:
            return Response(
                'Post is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, post)
        like_post(post, request.user)
        return Response('Success', status=status.HTTP_200_OK)
