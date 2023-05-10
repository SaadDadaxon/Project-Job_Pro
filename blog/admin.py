from django.contrib import admin
from .models import Blog, Comment


admin.site.register(Blog),


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'blog', 'body', 'parent_comment', 'top_level_comment_id', 'created_date')

