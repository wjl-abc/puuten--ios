from django.conf.urls.defaults import *

from ijustdated import views, models

urlpatterns = patterns('',
   
    # dating map
    url(r'^$', 'ijustdated.views.dating_map', name='dating_map'),
    
    # new dating
    url(r'^new/$', 'ijustdated.views.new_dating', name='new_dating'),
    
    #your dating
    url(r'^my_dating/$', 'ijustdated.views.my_dating', name='my_dating'),
    
    #details of a dating
    url(r'^details/(?P<id>\d+)/$', 'ijustdated.views.details', name="dating_details"),
    
    #comments to a diary
    url(r'^comment/(\d+)/$', 'ijustdated.views.comment', name='comment_diary'),
    
    #delete a diary
    url(r'^diary_destroy/(\d+)/$', 'ijustdated.views.diary_destroy', name='diary_destroy'),
    
    #delete a datingship
    url(r'^datingship_destroy/(\d+)/$', 'ijustdated.views.datingship_destroy', name='datingship_destroy'),
)