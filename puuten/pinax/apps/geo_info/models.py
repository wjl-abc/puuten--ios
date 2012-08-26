from django.db import models
from django.utils.translation import ugettext_lazy as _

class GeoInfo(models.Model):
    city      = models.CharField(_('city'), max_length=200)
    lat       = models.FloatField(_('latitude'))
    lng       = models.FloatField(_('longitude'))
