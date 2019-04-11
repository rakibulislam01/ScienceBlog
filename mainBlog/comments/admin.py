from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'object_id']


admin.site.register(Comment, CommentModelAdmin)
