from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    pages = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    follows = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    requests = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    liked_posts = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'role',
            'first_name',
            'last_name',
            'image_s3_path',
            'is_blocked',
            'pages',
            'follows',
            'requests',
            'liked_posts'
        ]
        read_only_fields = [
            'id',
            'image_s3_path',
            'is_blocked',
            'pages',
            'follows',
            'requests',
            'liked_posts'
        ]
