from django.db import models

class User(models.Model):
    address = models.CharField(max_length=100)
    handle = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    twitter_url = models.URLField(max_length=200)
    hometown = models.CharField(max_length=100)
    disc_handle = models.CharField(max_length=100)
    interests = models.CharField(max_length=200)

    def __str__(self):
        return self.handle
