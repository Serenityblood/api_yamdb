from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import CustomUser
from users.validators import validate_username


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(1, 'Не меньше 1'),
                    MaxValueValidator(10, 'Не больше 10')]
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Отзыв уже оставлен!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        model = Title

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для users."""

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

    def validate_username(self, value):
        validate_username(value)
        return value


class SingUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""
    username = serializers.CharField(max_length=settings.USERNAME_SIZE,
                                     validators=[validate_username])
    email = serializers.EmailField(max_length=settings.EMAIL_SIZE)


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(max_length=settings.USERNAME_SIZE,
                                     validators=[validate_username])
    confirmation_code = serializers.CharField(
        max_length=settings.CONF_CODE_SIZE
    )


class MeSerializer(UserSerializer):
    """Сериализатор для users/me."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
