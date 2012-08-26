from django import forms
from share.models import Share

class ShareForm(forms.ModelForm):

    class Meta:
        model = Share
        exclude = ('owner', 'shared_type', 'share_id', 'created_at')
