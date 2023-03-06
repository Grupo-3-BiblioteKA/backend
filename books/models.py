from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    year = models.IntegerField()
    sinopsy = models.CharField(max_length=255, null=True)
    pages = models.IntegerField()
