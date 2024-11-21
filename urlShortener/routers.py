from rest_framework.routers import DefaultRouter
from .views import URLShortenerModelViewset

url_router_v1 = DefaultRouter()
url_router_v1.register(r'shorten', URLShortenerModelViewset, basename='url-shortener')

