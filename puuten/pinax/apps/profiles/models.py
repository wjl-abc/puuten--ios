from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from timezones.fields import TimeZoneField

class Profile(models.Model):
    
    Visible_Choices = (
                      (1, _('Public')),
                      (2, _('Only to my friends')),
                      (3, _('None')),
                      )
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)
    about = models.TextField(_('about'), null=True, blank=True)
    latitude = models.FloatField(_('latitude'), default=39.904214)
    longitude = models.FloatField(_('longitude'), default=116.407413)
    scale = models.IntegerField(_('scale'), default=10)
    NE_lat = models.FloatField(_('NE_lat'), null=True, blank=True)
    NE_lng = models.FloatField(_('NE_lng'), null=True, blank=True)
    SW_lat = models.FloatField(_('SW_lat'), null=True, blank=True)
    SW_lng = models.FloatField(_('SW_lng'), null=True, blank=True)
    website = models.URLField(_('website'), null=True, blank=True, verify_exists=False)
    visible_to = models.IntegerField(_('visible'), choices=Visible_Choices, default=1)

    def __unicode__(self):
        return self.user.username
   
    def get_absolute_url(self):
        return ('profile_detail', None, {'id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
