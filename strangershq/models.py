from django.db import models

class User(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    twitter_id = models.CharField(max_length=100)
    token_id = models.CharField(max_length=100)
    twitter_pfp_url = models.URLField(max_length=200)
    hometown = models.CharField(max_length=100)
    discord_handle = models.CharField(max_length=100)
    interests = models.CharField(max_length=200)

    class Meta:
        db_table = 'wallet_information_testenv'
