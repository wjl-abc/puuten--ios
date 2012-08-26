from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from business_sina.models import BSInfo

class BSInfoForm(forms.ModelForm):
    
    class Meta:
        model = BSInfo
        exclude = ('new_name','sina_id', 'followed_by_id', 'address', 'phone_number', 'email', 'qq', 'introduction', 'tags', 'avatar', 'p_or_b', 'varified_or_not', 'created_at', 'updated_at', 'created_by', 'updated_by', 'status')
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BSInfoForm, self).__init__(*args, **kwargs)
    
