from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from business.models import BusinessProfile

class Contact(models.Model):
    business = models.ForeignKey(BusinessProfile, related_name="business_contact")
    address  = models.CharField(_('address'), max_length=200, blank=True, null=True)
    email    = models.CharField(_('email'), max_length=200, blank=True, null=True)
    number   = models.CharField(_('number'), max_length =200, blank=True, null=True)
    schedule = models.TextField(_('schedule'), blank=True, null=True)
    direction= models.TextField(_('direction'), blank=True, null=True)

    def __unicode__(self):
        return self.business
    
    def get_absolute_url(self):
        return ('business_contact', None, {
                'business_id': business.id
    })
    get_absolute_url = models.permalink(get_absolute_url)