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

"""Access Mode"""
ACCESSING_CHOICES = (
    (1, _('All the users')),
    (2, _('Only to those who have been approved by the creator')),
    (3, _('Only to those who are invited by creator')),
)

"""Invitation Mode"""
INVITE_STATUS = (
    (1, _('Created')),
    (2, _('Sent')),
    (3, _('Failed')),
    (4, _('Accepted')),
    (5, _('Declined')),
    (6, _('Deleted')),
)

"""
Join mode settings
"""
JOIN_MODE_STATUS = (
    (1, _('Open to all')),
    (2, _('Open to those approved by me')),
                    )

class Affair(models.Model):
    creator         = models.ForeignKey(User, related_name='creator_for_affair')
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'), default=datetime.now)
    theme           = models.CharField(_('theme'), max_length=200)
    tags            = TagField() 
    introduction    = models.TextField(_('introduction'))       
    latitude        = models.FloatField(_('latitude'), blank=True)
    longitude       = models.FloatField(_('longitude'), blank=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)
    join_mode       = models.IntegerField(_('joining setting'), choices=JOIN_MODE_STATUS, default=1)
    accessing_mode  = models.IntegerField(_('Open to'), choices=ACCESSING_CHOICES, default=1)
    def get_absolute_url(self):
        return ("affair_details", None, {'id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_type(self):
        return type(self).__name__.lower()
    
class AffairRelationShip(models.Model):
    partner     = models.ForeignKey(User, related_name="affair_invitations_from")
    affair_type = models.ForeignKey(ContentType)
    affair_id   = models.PositiveIntegerField()
    affair      = generic.GenericForeignKey('affair_type','affair_id')
    message     = models.TextField()
    sent        = models.DateField(default=datetime.now)
    status      = models.IntegerField(_('status'), choices=INVITE_STATUS, default=2)
    
    
class AffairDiary(models.Model):
    author      = models.ForeignKey(User, related_name='creator_for_affair_diary')
    affair_type = models.ForeignKey(ContentType)
    affair_id   = models.PositiveIntegerField()
    affair      = generic.GenericForeignKey('affair_type','affair_id')
    body        = models.TextField(_('diary'))
    tags        = TagField()
    latitude    = models.FloatField(_('latitude'), blank=True)
    longitude   = models.FloatField(_('longitude'), blank=True)
    created_at  = models.DateTimeField(_('created at'), default=datetime.now)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)
