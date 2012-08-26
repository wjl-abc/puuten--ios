from django.conf.urls.defaults import *
from share import views, models
from share.forms import *

urlpatterns = patterns('',
    # your share
    url(r'^$', 'share.views.your_share', name='your_share'),
    
    #destory blog post
    url(r'^destroy/(\d+)/$', 'share.views.destroy', name='share_destroy'),
)
