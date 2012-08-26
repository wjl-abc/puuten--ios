from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from photologue.models import *

from tagging.fields import TagField

from django.utils.translation import ugettext_lazy as _

PUBLISH_CHOICES = (
    (1, _('Public')),
    (2, _('Private')),
)

class PhotoSet(models.Model):
    """
    A set of photos
    """
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    publish_type = models.IntegerField(_('publish_type'), choices=PUBLISH_CHOICES, default=1)
    tags = TagField()
    animation       = models.IntegerField(_('owner_id'), blank=True, null= True, default=0)
    flag            = models.BooleanField(_('flag'), default=True)
    animation_updated_at = models.DateTimeField(_('created at'), default=datetime.now)

    class Meta:
        verbose_name = _('photo set')
        verbose_name_plural = _('photo sets')

class Image(ImageModel):
    """
    A photo with its details
    """
    SAFETY_LEVEL = (
        (1, _('Safe')),
        (2, _('Not Safe')),
    )
    Owner_Type_Choices = (
        (1, _('Person')),
        (2, _('Businss')),
    ),
    title = models.CharField(_('title'), max_length=200)
   # title_slug = models.SlugField(_('slug'))
   # caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public photographs will be displayed in the default views.'))
    member = models.ForeignKey(User, related_name="added_photos", blank=True, null=True)
    safetylevel = models.IntegerField(_('safetylevel'), choices=SAFETY_LEVEL, default=1)
    photoset = models.ManyToManyField(PhotoSet, blank=True, verbose_name=_('photo set'))
    tags = TagField()
    latitude        = models.FloatField(_('latitude'), blank=True, null= True)
    longitude       = models.FloatField(_('longitude'), blank=True, null= True)
    owner_type      = models.IntegerField(_('owner_type'), choices=Owner_Type_Choices, default=1)
    owner_id        = models.IntegerField(_('owner_id'), blank=True, null= True)
    animation       = models.IntegerField(_('animation'), blank=True, null= True, default=0)
    flag            = models.BooleanField(_('flag'), default=True)
    animation_updated_at = models.DateTimeField(_('created at'), default=datetime.now)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ("photo_details", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_type(self):
        return type(self).__name__.lower()

class Pool(models.Model):
    """
    model for a photo to be applied to an object
    """

    photo = models.ForeignKey(Image)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    created_at = models.DateTimeField(_('created_at'), default=datetime.now)

    class Meta:
        # Enforce unique associations per object
        unique_together = (('photo', 'content_type', 'object_id'),)
        verbose_name = _('pool')
        verbose_name_plural = _('pools')
