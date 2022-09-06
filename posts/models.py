from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post_date = models.DateTimeField(default=timezone.now)
    post_content = models.TextField()
    post_summary = models.TextField()
    post_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    post_image = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    show_post = models.BooleanField(default=False)
