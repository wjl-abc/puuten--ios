from django.conf.urls.defaults import *

from wat import views, models

urlpatterns = patterns('',
   
    #buzz map
    url(r'^$', 'wat.views.buzz_map', name='buzz_map'),
    
    #new buzz
    url(r'^new/$', 'wat.views.new_buzz', name='new_buzz'),
    
    #your buzz
    url(r'^your_buzz/$', 'wat.views.your_buzz', name='your_buzz'),
    
    #buzz details
    url(r'^details/(?P<id>\d+)/$', 'wat.views.details', name="buzz_details"),
    
    #comments to a diary
    url(r'^comment/(\d+)/$', 'wat.views.comment', name='buzz_comment_diary'),
    
    #delete a diary
    url(r'^diary_destroy/(\d+)/$', 'wat.views.diary_destroy', name='buzz_diary_destroy'),
    
    #delete a buzzship
    url(r'^buzzship_destroy/(\d+)/$', 'wat.views.buzzship_destroy', name='buzzship_destroy'),
    
    #edit a buzz
    url(r'^edit/(\d+)/$', 'wat.views.edit', name='buzz_edit'),
   
    #buzz admin
    url(r'^admin/(\d+)/$', 'wat.views.admin', name='buzz_admin'),
)