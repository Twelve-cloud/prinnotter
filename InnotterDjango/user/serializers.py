from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        max_length=1,
        default=User.Roles.USER,
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

    liked_posts = serializers.PrimaryKeyRelatedField(
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
            'liked_posts',
        ]
        read_only_fields = [
            'id',
            'image_s3_path',
            'is_blocked',
            'pages',
            'follows',
            'requests',
            'liked_posts',
        ]

    def create(self, validated_data):
        if validated_data['role'] == User.Roles.ADMIN:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        role = validated_data.get('role', instance.role)
        instance.is_staff = True if role == User.Roles.ADMIN else False
        instance.is_superuser = True if role == User.Roles.ADMIN else False
        return super().update(instance, validated_data)
