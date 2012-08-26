from django import template
from django.utils.translation import ugettext
from friends.models import Friendship
from friends.forms import InviteFriendForm

register = template.Library()

def show_profile(request, user):
    if request.user == user:
        is_me = True
    else:
        is_me = False
    is_friend = Friendship.objects.are_friends(request.user, user)
    invite_form = InviteFriendForm(request.user, {
                    'to_user': user.username,
                    'message': ugettext("Let's be friends!"),
                    })
    return {"user": user, 
            "is_me": is_me,
            "is_friend":is_friend, 
            "invite_form": invite_form}
register.inclusion_tag("profile_item.html")(show_profile)

def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path
register.simple_tag(clear_search_url)

def friends_checkbox(user):
    friendship = Friendship.objects.friends_for_user(user)
    friends = []
    for instance in friendship:
        friends.append(instance["friend"])
    head = """<div id='friends_list'>"""
    foot = """</div>"""
    body = """"""
    for instance in friends:
        body = body + """<input type='checkbox' name='items' value=%s />%s<br/>"""% (instance.id, instance.username)
    result = head+ body + foot
    return result
register.simple_tag(friends_checkbox)
