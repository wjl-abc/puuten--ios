import urllib

from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.hashcompat import md5_constructor

from action_record.models import *
from business_sina.models import BSInfo
from business_sina_weibo.models import WeiBo

register = template.Library()

@register.inclusion_tag("action_item.html")
def show_action(action_id):
    action = Action.objects.get(pk=action_id)
    return {"performer":action.performer,
            "act": action.act,
            "object": action.object}
    
@register.inclusion_tag("show_wish.html")
def show_wish(performer, wish):
    bs = BSInfo.objects.get(sina_id=wish.shared.sina_userid)
    return {"bs":bs,
            "performer":performer,
            "wb":wish.shared}

@register.inclusion_tag("show_wat.html")
def show_wat(performer, buzz):
    wb = WeiBo.objects.get(pk =buzz.reference_wb)
    bs = BSInfo.objects.get(sina_id=wb.sina_userid)
    creator = buzz.creator
    return {"creator":creator,
            "bs":bs,
            "wb":wb,
            "url":buzz.get_absolute_url()
            }