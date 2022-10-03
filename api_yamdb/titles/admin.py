from django.contrib import admin

from reviews.models import Comment, Review
from .models import Category, Genre, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('review', 'author')
    empty_value_display = '--пусто--'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author', 'score')
    empty_value_display = '--пусто--'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--пусто--'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--пусто--'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category', 'name', 'year', 'description', 'get_genres'
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category')
    empty_value_display = '--пусто--'

    def get_genres(self, obj):
        return '\n'.join([str(genre) for genre in obj.genre.all()])
