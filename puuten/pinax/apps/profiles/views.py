import datetime
import random
from django.utils import simplejson as json
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings

from notification.models import *
from notification.decorators import basic_auth_required, simple_basic_auth_callback
from notification.feeds import NoticeUserFeed

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404

from django.utils.translation import ugettext

from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship

from microblogging.models import Tweet, TweetInstance, Following
from microblogging.forms import TweetForm
from blog.models import Post
from photos.models import Image, Pool

from profiles.models import Profile
from profiles.forms import ProfileForm

from avatar.templatetags.avatar_tags import avatar
from threadedcomments.models import ThreadedComment

from account.models import Account, RegisterCode

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def profiles(request, template_name="profiles/profiles.html", extra_context=None):
    if extra_context is None:
        extra_context = {}
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
    }, **extra_context), context_instance=RequestContext(request))


def profile(request, id, template_name="profiles/profile.html", extra_context=None):
    if extra_context is None:
        extra_context = {}
    
    other_user = get_object_or_404(User, id=id)
    if "mobile" in request.POST: 
        other_user_profile = other_user.get_profile()
        result = {"name":other_user_profile.name, "about":other_user_profile.about}
        print result
        data = json.dumps(result)
        return HttpResponse(data)
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        is_following = Following.objects.is_following(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        other_friends = []
        is_friend = False
        is_me = False
        is_following = False
    
    other_user_profile = Profile.objects.get(user = other_user)
    if other_user_profile.visible_to == 1:
        visible = True
    elif other_user_profile.visible_to == 2:
        if is_friend:
            visible = True
        elif is_me:
            visible = True
        else:
            visible = False
    else:
        if is_me:
            visible = True
        else:
            visible = False
        
 
    if is_friend:
        invite_form = None
        previous_invitations_to = None
        previous_invitations_from = None
        if request.method == "POST":
            if request.POST.get("action") == "remove": # @@@ perhaps the form should just post to friends and be redirected here
                Friendship.objects.remove(request.user, other_user)
                request.user.message_set.create(message=_("You have removed %(from_user)s from friends") % {'from_user': other_user})
                is_friend = False
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Let's be friends!"),
                })
    
    else:
        if request.user.is_authenticated() and request.method == "POST":
            if request.POST.get("action") == "invite": # @@@ perhaps the form should just post to friends and be redirected here
                invite_form = InviteFriendForm(request.user, request.POST)
                if invite_form.is_valid():
                    invite_form.save()
            else:
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Let's be friends!"),
                })
                invitation_id = request.POST.get("invitation", None)
                if request.POST.get("action") == "accept": # @@@ perhaps the form should just post to friends and be redirected here
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.accept()
                            request.user.message_set.create(message=_("You have accepted the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
                            is_friend = True
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
                elif request.POST.get("action") == "decline": # @@@ perhaps the form should just post to friends and be redirected here
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.decline()
                            request.user.message_set.create(message=_("You have declined the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
        else:
            invite_form = InviteFriendForm(request.user, {
                'to_user': other_user.username,
                'message': ugettext("Let's be friends!"),
            })
    
    previous_invitations_to = FriendshipInvitation.objects.invitations(to_user=other_user, from_user=request.user)
    previous_invitations_from = FriendshipInvitation.objects.invitations(to_user=request.user, from_user=other_user)
    
    notice_types = NoticeType.objects.all()
    notices = Notice.objects.notices_for(request.user, on_site=True)
    settings_table = []
    for notice_type in notice_types:
        settings_row = []
        for medium_id, medium_display in NOTICE_MEDIA:
            form_label = "%s_%s" % (notice_type.label, medium_id)
            setting = get_notification_setting(request.user, notice_type, medium_id)
            if request.method == "POST":
                if request.POST.get(form_label) == "on":
                    setting.send = True
                else:
                    setting.send = False
                setting.save()
            settings_row.append((form_label, setting.send))
        settings_table.append({"notice_type": notice_type, "cells": settings_row})
    return render_to_response(template_name, dict({
    "visible": visible,
    "notices": notices,
    "notice_types": notice_types,
    "is_me": is_me,
    "is_friend": is_friend,
    "is_following": is_following,
    "other_user": other_user,
    "other_friends": other_friends,
    "invite_form": invite_form,
    "previous_invitations_to": previous_invitations_to,
    "previous_invitations_from": previous_invitations_from,
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def profile_edit(request, form_class=ProfileForm, **kwargs):
    template_name = kwargs.get("template_name", "profiles/profile_edit.html")
    if "mobile" in request.POST: 
        print 444444444
 #   if request.is_ajax():
 #       template_name = kwargs.get(
 #           "template_name_facebox",
 #           "profiles/profile_edit_facebox.html"
 #       )
    profile = request.user.get_profile()
    if request.method == "POST":
        profile_form = form_class(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.username = profile.name
            request.user.save()
            return HttpResponseRedirect(reverse("profile_detail", args=[request.user.id]))
    else:
        profile_form = form_class(instance=profile)
    return render_to_response(template_name,{
        "profile_form":profile_form,
        "profile": profile,
    }, context_instance=RequestContext(request))
