from django.contrib import admin

from users.modes import CustomUser
from .models import Category, Genre, Title, Review, Comment


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'bio', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '--пусто--'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'title', 'review')
    search_fields = ('text',)
    list_filter = ('review', 'author')
    empty_value_display = '--пусто--'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author', 'score')
    empty_value_display = '--пусто--'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'year', 'description')
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')
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
