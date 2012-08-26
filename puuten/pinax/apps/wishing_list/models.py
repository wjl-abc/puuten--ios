from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from share.models import *
from tagging.fields import TagField
from tagging.models import Tag

STATUS_CHOICES = (
    (1, _('Wating')),
    (2, _('Realized')),
)

VISIBLE_CHOICES = (
    (1, _('Public')),
    (2, _('Only to my friends')),    
)

CONNECTION_CHOICES = (
    (1, _('Applied')),
    (2, _('Accepted')),
    (3, _('Refuse')),
)
SCORE_CHOICES = (
    (1, _('Great')),
    (2, _('Fair')),
    (3, _('Not Bad')),
)

class Wish(Share):
    tags   = TagField(_('tags'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    visible = models.IntegerField(_('visible'), choices=VISIBLE_CHOICES, default=1)
    
    def get_type(self):
        return type(self).__name__.lower()

class Wish_Realize(models.Model):
    wish_type     = models.ForeignKey(ContentType, related_name="wish_type")
    wish_id       = models.PositiveIntegerField()
    wish          = generic.GenericForeignKey('wish_type','wish_id')
    realized_type = models.ForeignKey(ContentType, related_name="realized_type")
    realized_id   = models.PositiveIntegerField()
    realized      = generic.GenericForeignKey('realized_type', 'realized_id')
    status        = models.IntegerField(_('status'), choices=CONNECTION_CHOICES, default=1)
    score         = models.IntegerField(_('status'), choices=SCORE_CHOICES, default=1)
