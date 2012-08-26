import urllib

from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.hashcompat import md5_constructor

from avatar import AVATAR_DEFAULT_URL, AVATAR_GRAVATAR_BACKUP, AVATAR_GRAVATAR_DEFAULT
from profiles.models import Profile

register = template.Library()
    

def show_action(action_id):
    print action_id
    #action = Action.objects.all()
    temp = User.objects.get(pk=1)
    print temp
    #print len(action)
    #print temp.performer
    return temp
register.simple_tag(show_action)