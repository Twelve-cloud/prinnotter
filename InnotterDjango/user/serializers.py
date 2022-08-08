from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    pages = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    follows = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    requests = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    likes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password',
            'role', 'image_s3_path', 'is_blocked',
            'pages', 'follows', 'requests', 'likes'
        ]
        read_only_fields = [
            'id', 'pages', 'follows', 'requests', 'likes'
        ]
