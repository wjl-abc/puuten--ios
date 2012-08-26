from django import forms
from info_glue.models import Glueship

class GlueshipForm(forms.ModelForm):

    class Meta:
        model = Glueship
        exclude = ('created_at')
