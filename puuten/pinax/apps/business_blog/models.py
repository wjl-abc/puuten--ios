from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag

from blog.models import *

class BusinessBlog(Post):

    tags_extra            = TagField(_('tags'))
    def __unicode__(self):
        return self.title
    
#    url(r'^blogs/(?P<business_id>\d+)/(?P<blog_id>\d+)/$', 'blog.views.blog', name='business_blog'),
    def get_absolute_url(self):
        return ('business_blog', None, {
                'business_id':self.owner_id,
                'blog_id':self.id
    })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_edit_url(self):
        return ('business_blog_edit', None, {
                'business_id':self.owner_id,
                'blog_id':self.id                              
    })
    get_edit_url = models.permalink(get_edit_url)
    
    def get_destroy_url(self):
        return ('business_blog_destroy', None, {
                'business_id':self.owner_id,
                'blog_id':self.id                              
    })
    get_destroy_url = models.permalink(get_destroy_url)
    
    def get_type(self):
        return type(self).__name__.lower()

    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        super(BusinessBlog, self).save(force_insert, force_update)
    