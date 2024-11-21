from django.db import models
from datetime import datetime, timedelta



class URLShortener(models.Model):
    short_url = models.CharField(max_length=100, verbose_name="Shortened URL Alias", unique=True)
    original_url = models.CharField(max_length=100, verbose_name="Long URL", unique=True)
    custom_alias = models.CharField(max_length=100, verbose_name="User Suggested Alias", null=True)
    alias = models.CharField(max_length=100, verbose_name="Alias", null=True)
    ttl_seconds = models.IntegerField(default=120, null=True)
    expiry_time = models.DateTimeField(null=True, blank=True, verbose_name="Expiry time in seconds")
    visits_frequency = models.IntegerField(default=0, verbose_name="Count of user visits on this URL")
    last_accessed = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.id} - {self.short_url}"
    
