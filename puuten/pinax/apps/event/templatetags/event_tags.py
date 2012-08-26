# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from business.models import BusinessProfile

register = template.Library()


@register.inclusion_tag("event/event_item.html")
def show_event(event):
    return {"event": event}

def owner(event):
    business = BusinessProfile.objects.get(pk = event.owner_id)
    return """<a href="%s">%s</a>"""% (business.get_absolute_url(), business.name)
register.simple_tag(owner)

def event_window_info(event):
    business = BusinessProfile.objects.get(pk = event.owner_id)
    return """<div><h2><a href="%s">%s</a></h2><br><div><h4><a href="%s">%s</h4></div></div>"""% (business.get_absolute_url(), business.name, event.get_absolute_url(), event.title)
register.simple_tag(event_window_info)
