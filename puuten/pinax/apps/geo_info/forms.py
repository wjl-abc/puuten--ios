from django import forms
from django.utils.translation import ugettext_lazy as _

from geo_info.models import GeoInfo

class GeoInfoForm(forms.ModelForm):
    
    class Meta:
        model = GeoInfo
        exclude = ()
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(GeoInfoForm, self).__init__(*args, **kwargs)
    