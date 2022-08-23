from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User


class SignInSerializer(serializers.Serializer):
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

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        if user.is_blocked:
            raise serializers.ValidationError(
                'This user has been blocked.'
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, role='u')
