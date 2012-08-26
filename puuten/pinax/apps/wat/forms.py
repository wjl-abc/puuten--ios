from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from wat.models import Buzz, BuzzDiary

class BuzzForm(forms.ModelForm):
    
    class Meta:
        model = Buzz
        exclude = ('creator', 'created_at', 'updated_at', 'title', 'tags', 'accessing_mode', 'visibility_mode')
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BuzzForm, self).__init__(*args, **kwargs)
        
class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)
class BuzzDiaryForm(UserForm):
    tags = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField(label="Message", required=False, widget=forms.Textarea(attrs = {'cols': '20', 'rows': '5'}))
    def save(self):
        tags    = self.cleaned_data["tags"]
        message = self.cleaned_data["message"]
        buzz_diray = BuzzDiary(tags=tags, body=message)
        buzz_diray.save()
        return buzz_diary
