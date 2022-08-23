from rest_framework import serializers
from user.models import User


<<<<<<< HEAD
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

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, role='u')


=======
>>>>>>> 59f9326 (fix: some fixes)
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
