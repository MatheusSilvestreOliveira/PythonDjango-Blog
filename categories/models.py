from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=20)
