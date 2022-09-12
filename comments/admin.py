from django.contrib import admin
from .models import Comments


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_name', 'comment_email', 'comment_post', 'comment', 'comment_date', 'comment_show')
    list_editable = ('comment_show',)
    list_display_links = ('id', 'comment_name',)


admin.site.register(Comments, CommentAdmin)
