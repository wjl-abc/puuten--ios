#coding=gb2312
from django import template
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.hashcompat import md5_constructor
from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship
from django.contrib.auth.models import User

from microblogging.models import Following
from django.utils.safestring import mark_safe

from profiles.models import Profile
from profiles.forms import ProfileForm
import urllib
from django.utils import simplejson as json
from django.db.models import Q
from tagging_utils.models import PuuterTag

register = template.Library()

@register.inclusion_tag('tag_app/recommend_friends.html')
def show_recommendation_friends(other_user):
    other_friends = Friendship.objects.friends_for_user(other_user)
    friends = [otherfriend['friend'] for otherfriend in other_friends ]
    '''
    for otherfriend in other_friends:
        friends.extend([otherfriend['friend']])
    friends = [1,2]
    '''    
    profile = get_object_or_404(User, id=other_user.id).get_profile()
    
    friends.append(profile)#将自己也添加到排除列表中
    
    '''
    profiles = get_recommendationprofiles((profile.SW_lat + profile.NE_lat) /2.0,
                                          (profile.SW_lng + profile.NE_lng) /2.0,                                          
                                          20,
                                          friends
                                          )
    '''                                      
    profiles = get_recommendationprofiles(profile.SW_lat , profile.NE_lat,
                                          profile.SW_lng , profile.NE_lng,                                          
                                          20,
                                          friends
                                          )
    users = [_profile.user for _profile in profiles]
    #context["recommendprofiles"] = json.encode(str(obj2dict(profiles)))

    #json_profiles = { _profile.user.username:str(obj2dict(_profile)) for _profile in profiles }
    json_profiles = [{"uname":_profile.user.username,
                       "ulatitude":_profile.SW_lat,
                       "uotherlati":_profile.NE_lat,
                       "ulongitude":_profile.SW_lng,
                       "uotherlong":_profile.NE_lng
                       } for _profile in profiles ]
    
    return {"users":users,
            "recommendprofiles" : mark_safe(json.encode(json_profiles)),
            "mlatitude":profile.SW_lat,
            "motherlati":profile.NE_lat,
            "mlongitude":profile.SW_lng,
            "motherlong":profile.NE_lng
            }
     


def get_recommendationprofiles(latitude, otherlatitude, longitude, otherlongitude, num, excludeUsers, other = 0):
    """
    other 表示 一个多余的变动,可使范围变大或缩小(other为负)
    
    #经纬度在某个范围内,并排除已是朋友关系的人,后续讨论了再决定是否排除关注与被关注的人    
    return Profile.objects.all().filter(
        Q(latitude__lte = (tlatitude+other)) & Q(otherlatitude__gte = (tlatitude - other)),
        Q(longitude__lte = (tlongitude + other)) & Q(otherlongitude__gte = (tlongitude - other)),
        Q(user__in = excludeUsers)
        )[:num]
    """
    return Profile.objects.all().filter(
        Q(SW_lat__gte = (latitude-other)) & Q(SW_lat__lte = (otherlatitude+other)) |
        Q(NE_lat__gte = (latitude - other))& Q(NE_lat__lte = (otherlatitude + other)) |
        Q(SW_lat__lte = (latitude+other)) & Q(NE_lat__gte = (latitude - other))
        ,                                
        Q(SW_lng__gte = (longitude-other)) & Q(SW_lng__lte = (otherlongitude+other)) |
        Q(NE_lng__gte = (longitude - other))& Q(NE_lng__lte = (otherlongitude + other)) |
        Q(SW_lng__lte = (longitude+other)) & Q(NE_lng__gte = (longitude - other))
        ).exclude(user__in = excludeUsers)[:num]
    
    #return Profile.objects.all()[:num]


def obj2dict(obj):
    """
    summary:
        将object转换成dict类型    
    """
    memberlist = [m for m in dir(obj)]
    _dict = {}
    for m in memberlist:
        if m[0] != "_" and not callable(m):
            _dict[m] = getattr(obj,m)

    return _dict

@register.inclusion_tag('tag_app/recommend_tags.html')
def show_recommendation_tags(other_user):
    profile = get_object_or_404(User, id=other_user.id).get_profile()    
    return {"recommendcatetags" :  PuuterTag.objects.filter(tag_type=1),
            "recommendfretags" :  PuuterTag.objects.filter(tag_type=3)
            }
