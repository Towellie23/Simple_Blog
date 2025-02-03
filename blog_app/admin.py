from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'id')
    search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at')
    search_fields = ('content',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
