from django.db import models


# Create your models here.

class Manga(models.Model):
    name = models.CharField(max_length=255)
    trans_name = models.CharField(max_length=255)
    detail_link = models.CharField(max_length=255)
    cover_img = models.CharField(max_length=255)
    latest = models.FloatField(default=0)
    download = models.FloatField(default=0)
    status = models.CharField(max_length=20)
    genres = models.CharField(max_length=255)
    translatable = models.BooleanField(default=False)


class Genres(models.Model):
    name = models.CharField(max_length=50)
    trans_name = models.CharField(max_length=50)
