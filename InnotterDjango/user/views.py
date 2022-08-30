from user.permissions import (
    IsNotAuthentificatedOrAdmin, IsUserOwnerOrAdmin, IsAdmin, IsUserOwner
)
from rest_framework.permissions import IsAuthenticated
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
        user = User.objects.get(pk=pk)
        user.is_blocked = request.data.get('is_blocked', False)
        user.save()
        return Response("Success", status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], serializer_class=PostSerializer)
    def liked_posts(self, request, pk=None):
        posts = request.user.liked_posts
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
