from django.conf.urls.defaults import *
from business import views, models
from business.forms import *


urlpatterns = patterns('',
    #single business store
    url(r'^single_business/(?P<id>[-\w]+)/$', 'business.views.single_business', name='single_business'),
    #business profile
    url(r'profile/(?P<id>[-\w]+)/$', 'business.views.business_profile', name='business_profile'),
    # your business
    url(r'^your_business/$', 'business.views.your_business', name='your_business'),
    # creat new business
    url(r'^new/$', 'business.views.new', name='business_new'),
    # edit business profile
    url(r'^edit/(\d+)/$', 'business.views.edit', name='business_edit'),
    # destroy a single business
    url(r'^destroy/(\d+)/$', 'business.views.destroy', name='business_destroy'),
    # search
    url(r'^(?P<id>[-\w]+)/search/', 'business.views.search', name='business_search'),
    # your collection
    url(r'^your_collection/$', 'business.views.your_collection', name='your_collection'),
    
    #app_page
    url(r'^apps/(\d+)/$', 'business.views.apps', name='business_apps'),
    # about
    url(r'^about/(\d+)/$', 'business.views.about', name='business_about'),
    # menu
    url(r'^menu/(\d+)/$', 'business.views.menu', name='business_menu'),
   
    #gallery
    url(r'^gallery/(\d+)/$', 'business.views.gallery', name='business_gallery'), 
    # location
    url(r'^location/(\d+)/$', 'business.views.location', name='business_location'),
    
    # event
    url(r'^events/(?P<business_id>\d+)/$', 'event.views.events', name='business_events'),
    url(r'^events/(?P<business_id>\d+)/(?P<event_id>\d+)/$', 'event.views.event', name='business_event'),
    url(r'^events/(?P<business_id>\d+)/(?P<event_id>\d+)/edit/$', 'event.views.edit', name='business_event_edit'),
    url(r'^events/(?P<business_id>\d+)/new/$', 'event.views.new', name='business_new_event'),
    url(r'^events/(?P<business_id>\d+)/(?P<event_id>\d+)/destroy/$', 'event.views.destroy', name='business_event_destroy'),
    url(r'^events/(?P<business_id>\d+)/(?P<event_id>\d+)/switch/', 'event.views.switch', name='business_event_switch'),
    
    # business blog
    url(r'^blogs/(?P<business_id>\d+)/$', 'business_blog.views.blogs', name='business_blogs'),
    url(r'^blogs/(?P<business_id>\d+)/new/$', 'business_blog.views.new', name='business_new_blog'),
    url(r'^blogs/(?P<business_id>\d+)/(?P<blog_id>\d+)/edit/$', 'business_blog.views.edit', name='business_blog_edit'),
    url(r'^blogs/(?P<business_id>\d+)/(?P<blog_id>\d+)/$', 'business_blog.views.blog', name='business_blog'),
    url(r'^blogs/(?P<business_id>\d+)/(?P<blog_id>\d+)/destroy/$', 'business_blog.views.destroy', name='business_blog_destroy'),
    
    # business photo
    url(r'^photos/(?P<business_id>\d+)/$', 'business_photos.views.photos', name='business_photos'),
    url(r'^photos/(?P<business_id>\d+)/new/$', 'business_photos.views.new', name='business_new_photo'),
    url(r'^photos/(?P<business_id>\d+)/keditorupload/new/[\w\W]*$', 'business_photos.views.keditorupload', name='business_keditoruploadnew_photo'),
    url(r'^photos/(?P<business_id>\d+)/(?P<photo_id>\d+)/$', 'business_photos.views.photo', name='business_photo'),
    url(r'^photos/(?P<business_id>\d+)/(?P<photo_id>\d+)/edit/$', 'business_photos.views.edit', name='business_photo_edit'),
    url(r'^photos/(?P<business_id>\d+)/(?P<photo_id>\d+)/destroy/$', 'business_photos.views.destroy', name='business_photo_destroy'),
    
    #app_management
    url(r'^app_management/$', 'business.views.app_management', name='business_app_management'),
    #app_edit
    url(r'^app_edit/(\d+)/$', 'business.views.app_edit', name='business_app_edit'),
    #app_delete
    url(r'^app_destroy/(\d+)/$', 'business.views.app_destroy', name='business_app_destroy'),
    
    #business from sina
    url(r'^bs_weibo_list/(?P<bs_id>\d+)/$', 'business_sina_weibo.views.bs_weibo_list', name='bs_weibo_list'),
    url(r'^bs_all_new_weibo_list/$', 'business_sina_weibo.views.bs_all_new_weibo_list', name='bs_all_new_weibo_list'),
    url(r'^wb/(\d+)/$', 'business_sina_weibo.views.weibo', name='weibo'),
    url(r'^wb_comments/(\d+)/$', 'business_sina_weibo.views.wb_comments', name='wb_comments'),
    url(r'^bs_rd_del/(\d+)/$', 'business_sina_weibo.views.recommendation_del', name='bs_rd_del'),
    url(r'^bs_new/$', 'business_sina.views.bs_new', name='bs_new'),
    url(r'^bs_location/$', 'business_sina.views.bs_location', name='bs_location'),
    url(r'^bs_del/(\d+)/$', 'business_sina.views.bs_del', name='bs_del'),
    url(r'^bs_edit/(\d+)/$', 'business_sina.views.bs_edit', name='bs_edit'),
    url(r'^bs_wb/wishing_list/(?P<wb_id>\d+)/$', 'business_sina_weibo.views.add_2_wishing_list', name='wb_2_wishing_list'),
)
