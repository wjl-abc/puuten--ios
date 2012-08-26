from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from business_blog.models import BusinessBlog
import uuid

class BusinessBlogForm(forms.ModelForm):
    class Meta:
        model = BusinessBlog
        exclude = ('markup', 'author', 'creator_ip', 'created_at', 'updated_at', 'publish', 'owner_type', 'latitude', 'longitude', 'owner_id',
                   'tags', 'animation', 'flag', 'animation_updated_at')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BusinessBlogForm, self).__init__(*args, **kwargs)
