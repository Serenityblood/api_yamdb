from rest_framework import serializers

from .models import User, Category, Genre, Title, Comment, Review


class EmailSerializer(serializers.EmailField):
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        read_only_field = ('role',)

    class ReviewSerializer(serializers.ModelSerializer):
        author = serializers.SlugRelatedField(
            read_only=True, slug_field='username'
        )

        def validate(self, data):
            if self.context['request'].method != 'POST':
                return data
            user = self.context['request'].user
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Отзыв уже оставлен!'
                )
            return data

        class Meta:
            fields = ('id', 'text', 'author', 'score', 'pub_date')
            model = Review
