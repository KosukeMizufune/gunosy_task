from django.db import models


class Article(models.Model):
    tag = models.CharField(max_length=10)
    doc = models.TextField()
    key = models.CharField(max_length=10, unique=True)
