from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'post_author', 'post_date', 'post_category', 'show_post',)
    list_editable = ('show_post',)
    list_display_links = ('post_title',)


admin.site.register(Post, PostAdmin)
