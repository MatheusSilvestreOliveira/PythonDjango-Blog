from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings
import os


class Post(models.Model):
    post_title = models.CharField(max_length=255, verbose_name='Title')
    post_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author')
    post_date = models.DateTimeField(default=timezone.now, verbose_name='Date')
    post_content = models.TextField()
    post_summary = models.TextField()
    post_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Category')
    post_image = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    show_post = models.BooleanField(default=False, verbose_name='Show')

    def __str__(self):
        return self.post_title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_img(self.post_image.name, 1000)

    @staticmethod
    def resize_img(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(img_path, optimize=True, quality=70)
        new_img.close()
