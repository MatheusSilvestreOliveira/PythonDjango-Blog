from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('post_title', 'post_author', 'post_date', 'post_category', 'show_post',)
    list_editable = ('show_post',)
    list_display_links = ('post_title',)
    summernote_fields = ('post_content',)


admin.site.register(Post, PostAdmin)
