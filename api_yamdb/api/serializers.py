from rest_framework import serializers

from .models import User, Category, Genre, Title, Comment, Review


class EmailSerializer(serializers.EmailField):
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


