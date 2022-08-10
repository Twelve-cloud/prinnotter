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
            'access_token': user.generate_access_token(),
            'refresh_token': user.generate_refresh_token()
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
            'id', 'image_s3_path', 'is_blocked',
            'pages', 'follows', 'requests', 'likes'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
