# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from business.models import BusinessProfile

register = template.Library()




def owner(blog):
    business = BusinessProfile.objects.get(pk = blog.owner_id)
    return """<a href="%s">%s</a>"""% (business.get_absolute_url(), business.name)
register.simple_tag(owner)

def business_blog_window_info(blog):
    business = BusinessProfile.objects.get(pk = blog.owner_id)
    return """<div><h2><a href="%s">%s</a></h2><br><div><h4><a href="%s">%s</h4></div></div>"""% (business.get_absolute_url(), business.name, blog.get_absolute_url(), blog.title)
register.simple_tag(business_blog_window_info)
