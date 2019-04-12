from django.contrib import admin
from .models import Comment


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'object_id']


admin.site.register(Comment, CommentModelAdmin)
