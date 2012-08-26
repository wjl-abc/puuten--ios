from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from contact.models import Contact
import uuid

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('business')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ContactForm, self).__init__(*args, **kwargs)
