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
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
