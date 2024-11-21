from rest_framework import serializers
from .models import URLShortener


class UrlShortenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = URLShortener
        fields = "__all__"
        
