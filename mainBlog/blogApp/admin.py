from django.contrib import admin
from .models import Post


# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'timestamp', 'updated']
    list_display_links = ['id']
    list_filter = ['updated', 'title']
    search_fields = ['title', 'content', 'id']
    list_editable = ['title']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
