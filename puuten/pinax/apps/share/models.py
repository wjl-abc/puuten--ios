from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag
class Share(models.Model):
    """Share model"""
    ENTITY_TYPE = (
        (1, "BLOG"),
        (2, "PHOTO"),
        (3, "TWETTER"),
        (4, "ALBUM"),
        (5, "PERSONAL PAGE"),
        (6, "BUSINESS PAGE"),
        (7, "GROUP PAGE"),
        (8, "BUSINESS"),
        (9, "EVENT"),
        (10, "BUSINESS_BLOG"),
    )
    
    """Content Type"""
    CONTENT_TYPE = (
        (1, _('Word')),
        (2, _('Image')),
    )
    owner        = models.ForeignKey(User, related_name="ownership")
    shared_type  = models.ForeignKey(ContentType)
    shared_id    = models.PositiveIntegerField()
    shared       = generic.GenericForeignKey('shared_type','shared_id')
    content_type = models.IntegerField(_('type'), choices=ENTITY_TYPE, default=1)
    created_at   = models.DateTimeField(_('created at'), default=datetime.now)
    additional   = models.CharField(max_length=200, blank=True)

    def get_type(self):
        return type(self.shared).__name__.lower()
