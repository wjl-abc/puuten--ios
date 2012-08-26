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
    
"""Dating Mode"""
STATUS_CHOICES = (
    (1, _('M&M')),
    (2, _('M&F')),
    (3, _('F&F')),
)

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

"""Default Datingship Mode"""
DATINGSHIP_STATUS = (
    (1, _('Automatically set he/she to be your default dating parting next time')),
    (2, _('Automatically accept his/her dating request')),
)

class Dating(models.Model):
    creator         = models.ForeignKey(User, related_name='creator_for_dating')
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'), default=datetime.now)
    dating_mode     = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    tags            = TagField()
    latitude        = models.FloatField(_('latitude'), blank=True)
    longitude       = models.FloatField(_('longitude'), blank=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)
    reference_bs    = models.IntegerField(_('reference_bs'), blank=True, null=True)
    reference_wb    = models.IntegerField(_('reference_wb'), blank=True, null=True)
    
    def get_absolute_url(self):
        return ("dating_details", None, {'id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_type(self):
        return type(self).__name__.lower()
    
class DatingShip(models.Model):
    partner     = models.ForeignKey(User, related_name="dating_invitations_from")
    dating_type = models.ForeignKey(ContentType)
    dating_id   = models.PositiveIntegerField()
    dating      = generic.GenericForeignKey('dating_type','dating_id')
    message     = models.TextField()
    sent        = models.DateField(default=datetime.now)
    status      = models.IntegerField(_('status'), choices=INVITE_STATUS, default=2)
    
class DefaultPartnerShip(models.Model):
    default_from_user = models.ForeignKey(User, related_name="default_invitations_from")
    default_to_user   = models.ForeignKey(User, related_name="default_invitations_to")
    default_status    = models.IntegerField(_('default status'), choices=DATINGSHIP_STATUS)
"""
��ҪһЩ��ע��������DefaultPartnerShip
A   B   1 or 2
if 1:
   A set B to be his/her default dating partner
if 2:
   A accept B's dating request automactically 
"""
    
class DatingDiary(models.Model):
    author      = models.ForeignKey(User, related_name='creator_for_dating_diary')
    dating_type = models.ForeignKey(ContentType)
    dating_id   = models.PositiveIntegerField()
    dating      = generic.GenericForeignKey('dating_type','dating_id')
    body        = models.TextField(_('diary'))
    tags        = TagField()
    latitude    = models.FloatField(_('latitude'), blank=True)
    longitude   = models.FloatField(_('longitude'), blank=True)
    created_at  = models.DateTimeField(_('created at'), default=datetime.now)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    visibility_mode = models.IntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=1)
