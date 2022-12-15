
# Не забываем зарегистрировать модели, иначе мы не увидим их в админке.
from django.contrib import admin
from .models import Post, Author, Category, Comment, PostCategory

# создаём новый класс для представления товаров в админке
class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые мы хотим видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in Comment._meta.get_fields()]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'authorRating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('subscribers')


class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'preview', 'contentType', 'author', 'createTime', 'rating', 'editTime')


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)

# admin.site.unregister(Post)
