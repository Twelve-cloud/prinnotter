from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=255,
        min_length=8,
        write_only=True
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'access_token': user.generate_token(type='access'),
            'refresh_token': user.generate_token(type='refresh')
        }


class UserSerializer(serializers.ModelSerializer):
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
            'id', 'email', 'username', 'password',
            'role', 'image_s3_path', 'is_blocked',
            'pages', 'follows', 'requests', 'liked_posts'
        ]
        read_only_fields = [
<<<<<<< HEAD
            'id', 'image_s3_path', 'is_blocked',
            'pages', 'follows', 'requests', 'liked_posts'
=======
            'id', 'pages', 'follows', 'requests', 'liked_posts'
>>>>>>> 25a77a2 (fix: some fixes)
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
