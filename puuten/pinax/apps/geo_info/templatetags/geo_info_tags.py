from django import template
from django.utils.translation import ugettext

from geo_info.models import GeoInfo

register = template.Library()

def get_init_lat(business):
    location = business.location.split(" ")[0]
    geo_info = GeoInfo.objects.get(city=location)
    return geo_info.lat
register.simple_tag(get_init_lat)

def get_init_lng(business):
    location = business.location.split(" ")[0]
    geo_info = GeoInfo.objects.get(city=location)
    return geo_info.lng
register.simple_tag(get_init_lng)