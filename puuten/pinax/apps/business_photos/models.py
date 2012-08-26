from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from photos.models import *


class BusinessImage(Image):
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('business_photo', None, {
                'business_id':self.owner_id,
                'photo_id':self.id
    })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_edit_url(self):
        return ('business_photo_edit', None, {
                'business_id':self.owner_id,
                'photo_id':self.id                              
    })
    get_edit_url = models.permalink(get_edit_url)
    
    def get_destroy_url(self):
        return ('business_photo_destroy', None, {
                'business_id':self.owner_id,
                'photo_id':self.id                              
    })
    get_destroy_url = models.permalink(get_destroy_url)
       
    def get_type(self):
        return type(self).__name__.lower()