from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from blog.models import Post

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('markup', 'author', 'creator_ip', 'created_at', 'updated_at', 'publish', 'owner_type', 'owner_id', 'animation', 'flag', 'animation_updated_at')
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BlogForm, self).__init__(*args, **kwargs)
    
