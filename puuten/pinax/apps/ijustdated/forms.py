from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from ijustdated.models import Dating, DatingDiary

class DatingForm(forms.ModelForm):
    
    class Meta:
        model = Dating
        exclude = ('creator', 'created_at', 'updated_at', 'dating_mode', 'visibility_mode')
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(DatingForm, self).__init__(*args, **kwargs)

class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
class DatingDiaryForm(UserForm):
    tags = forms.CharField(widget=forms.HiddenInput)
    #latitude = forms.FloatField(widget=forms.HiddenInput)
    #longitude = forms.FloatField(widget=forms.HiddenInput)
    message = forms.CharField(label="Message", required=False, widget=forms.Textarea(attrs = {'cols': '20', 'rows': '5'}))
    
    
    
    def save(self):
        tags     = self.cleaned_data["tags"]
        message = self.cleaned_data["message"]
        dating_diray = DatingDiary(tags=tags, body=message)
        dating_diray.save()
        return dating_diary
