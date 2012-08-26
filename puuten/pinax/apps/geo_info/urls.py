from django.conf.urls.defaults import *

from geo_info import views, models



urlpatterns = patterns('',
    #
    url(r'^$', 'geo_info.views.info', name='geo_info'),
    url(r'^destroy/(\d+)/$', 'geo_info.views.geo_info_destroy', name='geo_info_destroy'),
)
