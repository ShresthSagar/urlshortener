from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import URLShortener
from .serializers import UrlShortenerSerializer
from .services import UrlShortenerService as url_shortener_service
from rest_framework.decorators import action
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import datetime
from django.utils.timezone import now


# Create your views here.
class URLShortenerModelViewset(ModelViewSet):

    serializer_class = UrlShortenerSerializer
    queryset = URLShortener.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def shortened_url_response_mapper(self, long_url, short_url):
        return {"original_url": long_url, "short_url": short_url}


    def get_response_data_from_analytics_mapper(self, url_obj):
        return {
            "access_counts": url_obj.visits_frequency,
            "alias": url_obj.alias,
            "access_times": url_obj.last_accessed,
            "ttl": url_obj.ttl_seconds,
            "custom_alias": url_obj.custom_alias,
        }


    # Post
    def create(self, request, *args, **kwargs):
        try:
            long_url = request.data.get("long_url")
            custom_alias = request.data.get("custom_alias", None)
            ttl_seconds = request.data.get("ttl_seconds", None)
            short_url = url_shortener_service.get_short_url(long_url=long_url, custom_alias=custom_alias, ttl_seconds=ttl_seconds)
            return Response(data=self.shortened_url_response_mapper(long_url=long_url, short_url=short_url), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=["get"])
    def analytics(self, request, alias=None, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        url_obj = URLShortener.objects.get(custom_alias=alias)
        response_data = self.get_response_data_from_analytics_mapper(url_obj)
        return Response({"data": response_data}, status=status.HTTP_200_OK)


    
    # Patch
    def partial_update(self, request, pk=None):
        try:
            alias = pk
            custom_alias = request.data.get("custom_alias", None)
            ttl_seconds = request.data.get("ttl_seconds", None)
            url_object = url_shortener_service.update_url(alias, custom_alias, ttl_seconds)
            
            return Response(data=self.get_response_data_from_analytics_mapper(url_object), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

    
    # Delete
    def destroy(self, request, pk, *args, **kwargs):
        try:
            obj = URLShortener.objects.get(alias = pk)
            obj.delete()
            return Response(data={"data": "Url with alias {} is deleted".format(pk)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": "Url not found"}, status=status.HTTP_404_NOT_FOUND)

    


def get_redirect_url(request, alias):
    url_obj = URLShortener.objects.get(alias=alias)

    if url_obj.expiry_time <= now():
        return JsonResponse({"error": "url not found"}, status=404)
    url_obj.visits_frequency += 1
    last_accessed = url_obj.last_accessed
    url_obj.save()
    return HttpResponseRedirect(url_obj.original_url)


def get_analytics(request, alias):
    url_obj = URLShortener.objects.get(alias=alias)
    return JsonResponse({
            "access_counts": url_obj.visits_frequency,
            "alias": url_obj.alias,
            "access_times": url_obj.last_accessed,
            "ttl": url_obj.ttl_seconds,
            "custom_alias": url_obj.custom_alias,
            "expiry_time": url_obj.expiry_time,
        })