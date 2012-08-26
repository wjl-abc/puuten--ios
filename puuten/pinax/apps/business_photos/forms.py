from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from business_photos.models import BusinessImage
import uuid

class BusinessPhotoUploadForm(forms.ModelForm):
    
    class Meta:
        model = BusinessImage
        exclude = ('member', 'photoset', 'effect', 'crop_from', 'latitude', 'longitude', 'owner_type', 'owner_id')
        
    def clean_image(self):
        if '#' in self.cleaned_data['image'].name:
            raise forms.ValidationError(
                _("Image filename contains an invalid character: '#'. Please remove the character and try again."))
        self.cleaned_data['image'].name =  uuid.uuid1().__str__() + '.' + self.cleaned_data['image'].name.split('.')[-1]
        return self.cleaned_data['image']

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BusinessPhotoUploadForm, self).__init__(*args, **kwargs)

class BusinessPhotoEditForm(forms.ModelForm):
    
    class Meta:
        model = BusinessImage
        exclude = ('member', 'photoset', 'title_slug', 'effect', 'crop_from', 'image','latitude', 'longitude', 'owner_type', 'owner_id')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BusinessPhotoEditForm, self).__init__(*args, **kwargs)
