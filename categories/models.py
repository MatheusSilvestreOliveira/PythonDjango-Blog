from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=20, verbose_name='Category name')

    def __str__(self):
        return self.cat_name
