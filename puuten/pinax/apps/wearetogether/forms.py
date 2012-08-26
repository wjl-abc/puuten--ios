from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from wearetogether.models import *

class AffairForm(forms.ModelForm):
    
    class Meta:
        model = Affair
        exclude = ('creator', 'created_at', 'updated_at', 'visibility_mode', 'join_mode', )
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(AffairForm, self).__init__(*args, **kwargs)

class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
class AffairDiaryForm(UserForm):
    tags = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField(label="Message", required=False, widget=forms.Textarea(attrs = {'cols': '20', 'rows': '5'}))
    
    
    
    def save(self):
        tags     = self.cleaned_data["tags"]
        message = self.cleaned_data["message"]
        affair_diray = AffairDiary(tags=tags, body=message)
        affair_diray.save()
        return affair_diary
