# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from share.models import Share
from datetime import timedelta
from datetime import datetime

register = template.Library()


@register.simple_tag
def same_type_or_not(share_type, text):
    if share_type==ContentType.objects.get(model=text):
        return True
    else:
        return False
register.simple_tag(same_type_or_not)

def get_share_count(object):
    return ThreadedComment.objects.filter(shared_type=ContentType.objects.get(model=object.get_type()), shared_id=object.id).count()
register.simple_tag(get_share_count)

def get_share_count_from_T(object, T):
    return Share.objects.filter(shared_type=ContentType.objects.get(model=object.get_type()), shared_id=object.id, created_at=datetime.now()-timedelta(days=T)).count()
register.simple_tag(get_share_count_from_T)
