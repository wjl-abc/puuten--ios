from django.conf.urls.defaults import *

from wearetogether import views, models

urlpatterns = patterns('',
   
    # affair map
    url(r'^$', 'wearetogether.views.affair_map', name='affair_map'),
    
    # new affair
    url(r'^new/$', 'wearetogether.views.new_affair', name='new_affair'),
    
    # new invitation and management
    url(r'^management/(\d+)/$', 'wearetogether.views.management', name='affair_management'),
    
    # edit your affair
    url(r'^edit/(\d+)/$', 'wearetogether.views.edit_affair', name='affair_edit'),
    
    # my affair
    url(r'^my_affairs/$', 'wearetogether.views.my_affairs', name='my_affairs'),
    
    #affair details
    url(r'^details/(?P<id>\d+)/$', 'wearetogether.views.details', name="affair_details"),
    
    #comments to a diary
    url(r'^comment/(\d+)/$', 'wearetogether.views.comment', name='comment_affair_diary'),
    
    #delete a diary
    url(r'^affair_diary_destroy/(\d+)/$', 'wearetogether.views.affair_diary_destroy', name='affair_diary_destroy'),
    
    #delete a datingship
    url(r'^affairship_destroy/(\d+)/$', 'wearetogether.views.affairship_destroy', name='affairship_destroy'),
)