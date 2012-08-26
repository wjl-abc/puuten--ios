from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from blog.models import *
from tagging.fields import TagField
from tagging.models import Tag

class Event(Post):
    UPCOMING_OR_Not = (
        (1, _('Upcoming')),
        (2, _('Past')),
    )
    upcoming_or_not = models.IntegerField(_('upcoming_or_not'), choices=UPCOMING_OR_Not, default=1)
    tags_extra            = TagField(_('tags'))
    def __unicode__(self):
        return self.title
    
#    url(r'^events/(?P<business_id>\d+)/(?P<event_id>\d+)/$', 'event.views.event', name='business_event'),
    def get_absolute_url(self):
        return ('business_event', None, {
                'business_id':self.owner_id,
                'event_id':self.id
    })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_edit_url(self):
        return ('business_event_edit', None, {
                'business_id':self.owner_id,
                'event_id':self.id                              
    })
    get_edit_url = models.permalink(get_edit_url)
    
    def get_destroy_url(self):
        return ('business_event_destroy', None, {
                'business_id':self.owner_id,
                'event_id':self.id                              
    })
    get_destroy_url = models.permalink(get_destroy_url)
    
    def get_switch_url(self):
        return ('business_event_switch', None, {
                'business_id':self.owner_id,
                'event_id':self.id                              
    })
    get_switch_url = models.permalink(get_switch_url) 
    
    def get_type(self):
        return type(self).__name__.lower()

    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        super(Event, self).save(force_insert, force_update)
    