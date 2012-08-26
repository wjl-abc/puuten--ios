from datetime import datetime
from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Action(models.Model):
    Act_Type_Choices = (
        (1, _('create')),
        (2, _('update')),
        (3, _('accept')),
        (4, _('join')),
    )
    
    
    performer   = models.ForeignKey(User, related_name="performer")
    act         = models.IntegerField(_('act'), choices=Act_Type_Choices, default=1)
    object_type = models.ForeignKey(ContentType)
    object_id   = models.PositiveIntegerField()
    object      = generic.GenericForeignKey('object_type','object_id')
    additional  = models.CharField(max_length=200, blank=True)
    time        = models.DateTimeField(_('publish'), default=datetime.now)
    