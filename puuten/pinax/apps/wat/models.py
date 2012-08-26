#coding=utf-8
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

"""Visibility Mode"""
VISIBILITY_CHOICES = (
    (1, _('Public')),
    (2, _('Only open to my friends')),
    (3, _('Only open to me and my partner')),
)

"""Invitation Mode"""
INVITE_STATUS = (
    (1, _('Created')),
    (2, _('Sent')),
    (3, _('Failed')),
    (4, _('Accepted')),
    (5, _('Refused')),
    (6, _('Deleted')),
)

"""Accessing Mode"""
ACCESSING_STATUS = (
    (1, _('Users can join in freely.')),
    (2, _('Only open to those invited by me.')),
    (3, _('Both application and my approve are needed to join in.')),
)


class Buzz(models.Model):
    creator         = models.ForeignKey(User, related_name='creator_for_buzz')
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'), default=datetime.now)
    title           = models.CharField(_('theme'), max_length=200, blank=True)
    tags            = TagField()
    body            = models.TextField(_('body'), blank=True)
    latitude        = models.FloatField(_('latitude'), blank=True, null=True)
    longitude       = models.FloatField(_('longitude'), blank=True, null=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)
    accessing_mode  = models.IntegerField(_('accessing'), choices=ACCESSING_STATUS, default=1)
    reference_bs    = models.IntegerField(_('reference_bs'), blank=True, null=True)
    reference_wb    = models.IntegerField(_('reference_wb'), blank=True, null=True)
    
    
    def get_absolute_url(self):
        return ("buzz_details", None, {'id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_type(self):
        return type(self).__name__.lower()
    
class BuzzShip(models.Model):
    partner     = models.ForeignKey(User, related_name="buzz_invitations_from")
    buzz_type   = models.ForeignKey(ContentType)
    buzz_id     = models.PositiveIntegerField()
    buzz        = generic.GenericForeignKey('buzz_type','buzz_id')
    message     = models.TextField()
    sent        = models.DateField(default=datetime.now)
    status      = models.IntegerField(_('status'), choices=INVITE_STATUS, default=4)
        
class BuzzDiary(models.Model):
    author      = models.ForeignKey(User, related_name='creator_for_buzz_diary')
    buzz_type   = models.ForeignKey(ContentType)
    buzz_id     = models.PositiveIntegerField()
    buzz        = generic.GenericForeignKey('buzz_type','buzz_id')
    body        = models.TextField(_('diary'))
    tags        = TagField()
    latitude    = models.FloatField(_('latitude'), blank=True, null=True)
    longitude   = models.FloatField(_('longitude'), blank=True, null=True)
    created_at  = models.DateTimeField(_('created at'), default=datetime.now)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)