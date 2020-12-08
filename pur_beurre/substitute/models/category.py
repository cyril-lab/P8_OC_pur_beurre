from django.conf import settings
from django.db import models


class Category(models.Model):
    """this class is used to generate the category table"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.pk



# class Favorites(models.Model):
#     username = models.CharField(max_length=200)
#
#     favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favourite')

