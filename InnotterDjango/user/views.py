from user.permissions import (
    IsNotAuthentificatedOrAdmin, IsUserOwnerOrAdmin, IsAdmin, IsUserOwner
)
from rest_framework.permissions import IsAuthenticated
from user.services import get_user_by_id, set_blocking
from rest_framework.decorators import action
from rest_framework.response import Response
from user.serializers import UserSerializer
from blog.serializers import PostSerializer
from rest_framework import viewsets
from rest_framework import status
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    permission_map = {
        'create': (
            IsNotAuthentificatedOrAdmin,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated,
            IsUserOwnerOrAdmin,
        ),
        'partial_update': (
            IsAuthenticated,
            IsUserOwnerOrAdmin,
        ),
        'destroy': (
            IsAuthenticated,
            IsUserOwnerOrAdmin,
        ),
        'block': (
            IsAuthenticated,
            IsAdmin,
        ),
        'liked_posts': (
            IsAuthenticated,
            IsUserOwner
        )
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()

    @action(detail=True, methods=['patch'])
    def block(self, request, pk=None):
        user = get_user_by_id(pk)

        if not user:
            return Response(
                'User is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        set_blocking(user, request.data.get('is_blocked', False))
        return Response('Success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], serializer_class=PostSerializer)
    def liked_posts(self, request, pk=None):
        user = get_user_by_id(pk)

        if not user:
            return Response(
                'User is not found',
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, user)
        liked_posts = user.liked_posts
        serializer = self.serializer_class(liked_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
