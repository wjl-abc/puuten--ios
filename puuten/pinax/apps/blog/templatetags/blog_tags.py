# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from threadedcomments.templatetags.threadedcommentstags import get_comments_count

register = template.Library()


@register.inclusion_tag("blog/blog_item.html")
def show_blog_post(blog_post):
    return {"blog_post": blog_post}

def blog_window_info(blog):
    title = blog.title
    link = blog.get_absolute_url()
    avatar = avatar_user(blog.author.id, 40)
    author = blog.author.username
    author_url = blog.author.get_absolute_url()
    comments_count = get_comments_count(blog)
    comments_count = str(comments_count)
    info = '<h2><a href='+link+'>'+title+'</a></h2><br><div style="float: left;">'+avatar+'</div><a>'+comments_count+'</a><p><a href='+author_url+'>'+author+'</a></p>'
    return info
register.simple_tag(blog_window_info)
