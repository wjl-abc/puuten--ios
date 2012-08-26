import re

from django import template
from business_sina.models import BSInfo
from business_sina_weibo.models import WeiBo
from wat.models import BuzzShip

register = template.Library()


def get_member_count(instance):
    creator = instance.creator 
    buzz_ship = BuzzShip.objects.filter(buzz_id=instance.id, status=4).exclude(partner=creator)
    count = buzz_ship.count()
    return count
register.simple_tag(get_member_count)

def get_applicant_count(instance):
    buzz_ship = BuzzShip.objects.filter(buzz_id=instance.id, status=2)
    count = buzz_ship.count()
    return count
register.simple_tag(get_applicant_count)

@register.inclusion_tag("show_wat_invitation.html")
def show_wat_invitation(invitation):
    wb = WeiBo.objects.get(pk=invitation.buzz.reference_wb)
    return {"id":invitation.id,
            "from":invitation.buzz.creator,
            "info":invitation.message,
            "wb": wb}
    
@register.inclusion_tag("show_buzz.html")
def show_buzz(buzz):
    wb = WeiBo.objects.get(pk=buzz.reference_wb)
    bs = BSInfo.objects.get(sina_id=wb.sina_userid)
    return {"wb":wb,
            "bs":bs,
            "buzz":buzz
            }