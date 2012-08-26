from django.conf.urls.defaults import *

from wishing_list import views

urlpatterns = patterns('',
   
    #your wishing list
    url(r'^$', 'wishing_list.views.your_wishing_list', name='your_wishing_list'),
    
    #new wish
    url(r'^new/$', 'wishing_list.views.new', name='new_wish'),
    
    #wishing destroy
    url(r'^destroy/(\d+)/$', 'wishing_list.views.destroy', name='wishing_destroy'),
    
    #wishing and dating
    url(r'^and_dating/(\d+)/$', 'wishing_list.views.dating_and_wishing', name='dating_and_wishing'),
    
    #user list who add the object to his/her wishinglist
    url(r'^user_list/(?P<type_id>\d+)/(?P<shared_id>\d+)/$', 'wishing_list.views.user_list', name='wishing_list_user_list'),
)
