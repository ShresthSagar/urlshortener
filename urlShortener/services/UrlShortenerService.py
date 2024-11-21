from urlShortener.models import URLShortener
from django.conf import settings
import uuid
import random
from datetime import datetime, timedelta

from django.utils.timezone import now

def generate_short_url(custom_alias: str):
    my_domain = settings.MY_DOMAIN
    new_url = ""
    if custom_alias:
        new_url = my_domain + custom_alias + "/"
        return new_url, custom_alias
    else:
        alias = uuid.uuid1(random.randint(0, 281474976710655))
        new_url = my_domain + str(alias) + "/"
        return new_url, alias



def get_short_url(long_url: str, custom_alias: str, ttl_seconds: int=120):
    try:
        url_obj = URLShortener.objects.get(original_url=long_url)
        if url_obj:
            print("Previous short url was - ", url_obj.short_url, ". Generating New URL")
            new_short_url, alias = generate_short_url(custom_alias=custom_alias)
            url_obj.short_url = new_short_url
            url_obj.custom_alias = custom_alias
            url_obj.alias = alias
            url_obj.visits_frequency = 0
            url_obj.ttl_seconds = ttl_seconds
            url_obj.expiry_time = now()+ timedelta(seconds=ttl_seconds)
            url_obj.save()
            return new_short_url
    
    except URLShortener.DoesNotExist:
        print("Short url does not exist. Generating New...")
        new_short_url, alias = generate_short_url(custom_alias=custom_alias)
        expiry_time = now()+ timedelta(seconds=ttl_seconds)
        url_obj = URLShortener(short_url= new_short_url, original_url=long_url, ttl_seconds=ttl_seconds, custom_alias=custom_alias, alias=alias, expiry_time=expiry_time)
        url_obj.save()
        return new_short_url
    return None
    



def update_url(alias: str, custom_alias: str, ttl: int):

    url_object = URLShortener.objects.get(alias=alias)
    if ttl:
        url_object.ttl_seconds = int(ttl)
        url_object.expiry_time = now() + timedelta(seconds=int(ttl))
    if custom_alias:
        url_object.custom_alias = custom_alias
    url_object.save()
    return url_object


def get_total_visit_counts(short_url: str):
    url_object = URLShortener.objects.get(short_url=short_url)
    return url_object.visits_frequency
