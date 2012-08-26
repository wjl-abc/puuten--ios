from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from event.models import Event
import uuid

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('markup', 'author', 'creator_ip', 'created_at', 'updated_at', 'publish', 'owner_type', 'upcoming_or_not', 'latitude', 'longitude', 'owner_id',
                    'tags', 'animation', 'flag', 'animation_updated_at')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(EventForm, self).__init__(*args, **kwargs)
