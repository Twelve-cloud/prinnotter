from user.permissions import (
    IsNotAuthentificatedOrAdmin, IsUserOwnerOrAdmin
)
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserSerializer
from rest_framework import viewsets
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
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
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super(self.__class__, self).get_permissions()
