from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        lookup_fields = ('username')
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
            'email',
        )

    def __str__(self) -> str:
        return self.username


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, value):
        if 'me' == value:
            raise serializers.ValidationError('me - недоступно')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=500)


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = CustomUser
