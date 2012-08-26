import re

from django import template
from ijustdated.models import DatingShip
from profiles.models import Profile

register = template.Library()


def get_another_partner(instance):
    dating = instance.dating    
    datingship = DatingShip.objects.filter(dating_id=dating.id)
    if len(datingship)>1:
        if datingship[0]==instance:
            dating = datingship[1]
        else:
            dating = datingship[0]
        partner = dating.partner
        profile = Profile.objects.get(user=partner)
        user_url = profile.get_absolute_url()
        return """<div><p><a href="%s">%s</a></p></div>""" % (user_url, partner.username)
    else:
        return """<div><p><a>someone</a></p></div>"""
register.simple_tag(get_another_partner)

def window_info_dating(instance):
    datingship = DatingShip.objects.filter(dating_id=instance.id)
    if len(datingship)>1:
        partner1 = datingship[0].partner
        partner2 = datingship[1].partner
        profile1 = Profile.objects.get(user=partner1)
        profile2 = Profile.objects.get(user=partner2)
        user1_url = profile1.get_absolute_url()
        user2_url = profile2.get_absolute_url()
        return """<div><p><a href='%s'>%s</a><a href='%s'> %s</a><br/><a>%s</a></p></div>""" % (user1_url, partner1.username, user2_url, partner2.username, instance.tags)
    elif len(datingship)==1:
        partner1 = datingship[0].partner
        profile1 = Profile.objects.get(user=partner1)
        user1_url = profile1.get_absolute_url()
        return """<div><p><a href='%s'>%s</a></p></div>"""% (user1_url, partner1.username)
    else:
        return ""
register.simple_tag(window_info_dating)    
