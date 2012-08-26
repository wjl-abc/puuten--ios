from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

class BigIntegerField(models.IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"    
    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.

class BSAdmin(models.Model):
    b_s_admin        = models.ForeignKey(User, related_name="business_sina_admin")
    approved_or_not  = models.BooleanField(_('allow comments'), default=True)
    
    def b_s_admin_approved(self):
        return self.approved_or_not

IDENTITY_CHOICES = (
        (1, _('Person')),
        (2, _('Business')),
    )
STATUS_CHOICES  = (
        (1, _('active')),
        (2, _('negative')),
    )    
class BSInfo(models.Model):
    name     = models.CharField(_('name'), max_length=200, null=True, blank=True)
    new_name = models.CharField(_('new_name'), max_length=200, null=True, blank=True)
    sina_url = models.URLField(_('sina_url'), verify_exists=True)
    sina_id  = BigIntegerField(_('sina_id'), null=True, blank=True)
    followed_by_id = BigIntegerField(_('sina_id'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=200, null=True, blank=True)
    introduction = models.TextField(_('introduction'), null=True, blank=True)
    tags     = TagField()
    address  = models.CharField(_('address'), max_length=200, null=True, blank=True)
    phone_number = models.CharField(_('phone_number'), max_length=50, null=True, blank=True)
    email    = models.CharField(_('email'), max_length=50, null=True, blank=True)
    qq       = models.CharField(_('qq'), max_length=50, null=True, blank=True)
    latitude = models.FloatField(_('latitude'), default=39.904214)
    longitude = models.FloatField(_('longitude'), default=116.407413)
    avatar   = models.CharField(_('avatar'), max_length=200, null=True, blank=True)
    avatar_large   = models.CharField(_('avatar_large'), max_length=200, null=True, blank=True)
    p_or_b   = models.IntegerField(_('type'), choices=IDENTITY_CHOICES, default=2)
    varified_or_not = models.BooleanField(_('varified'), default=False)
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'), null=True, blank=True)
    created_by      = models.ForeignKey(User, related_name="b_s_admin_a")
    status   = models.IntegerField(_('type'), choices=STATUS_CHOICES, default=2)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('bs_weibo_list', None, {'bs_id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
        