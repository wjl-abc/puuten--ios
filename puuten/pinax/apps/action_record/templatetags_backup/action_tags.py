# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from threadedcomments.templatetags.threadedcommentstags import get_comments_count

register = template.Library()

def show_action(action_id):
    #print action_id
    print "#####"
    return action_id
register.simple_tag(show_action)
