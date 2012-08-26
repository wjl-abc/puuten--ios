import datetime
from datetime import datetime
from django.utils import simplejson as json
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext

from wearetogether.models import *
from wearetogether.forms import *
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from profiles.models import Profile

def affair_map(request, template_name="wearetogether/affair_map.html"):
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
    }, context_instance=RequestContext(request))
    
def new_affair(request, form_class=AffairForm, affair_relationship=AffairRelationShip, template_name="wearetogether/new_affair.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            affair_form = form_class(request.user, request.POST)
            if affair_form.is_valid():
                affair = affair_form.save(commit=False)
                affair.creator = request.user
                affair.save()
                affair_relationship_instance = affair_relationship(partner=request.user, affair=affair, message="", status=4)
                affair_relationship_instance.save()
                return HttpResponseRedirect(reverse("affair_management", args=(affair.id,)))
    return render_to_response(template_name,{
            "profile":request.user.get_profile(),
            "affair_form":form_class(),
        }, context_instance=RequestContext(request))

def management(request, id, template_name="wearetogether/management.html"):
    affair = Affair.objects.get(pk=id)
    if not affair:
        raise Http404
    if request.method == "POST":
        if not "action" in request.POST:
            users = User.objects.filter(username__icontains=request.POST["search_term"])
            data = [{"avatar": avatar_user(user.id, 40),
                     "username": user.username,
                     "link": Profile.objects.get(user=user).get_absolute_url(),
                     "id": user.id
                     }
                     for user in users]
            data = json.dumps(data)
            return HttpResponse(mark_safe(data))
        else:
            print request.POST
            print request.POST['invitation']
            print request.POST['message']
    return render_to_response(template_name,{
            "affair":affair,
        }, context_instance=RequestContext(request))

def edit_affair(request, id, form_class=AffairForm, template_name="wearetogether/edit_affair.html"):
    affair = Affair.objects.get(pk=id)
    if not affair:
        raise Http404
    if request.method == "POST":
        if affair.creator != request.user:
            request.user.message_set.create(message="You can't edit affairs that aren't yours")
            return HttpResponseRedirect(reverse("affair_management", args=(affair.id,)))
        if request.POST["action"] == "update":
            affair_form = form_class(request.user, request.POST, instance=affair)
            if affair_form.is_valid():
                affair = affair_form.save(commit=False)
                affair.save()
                request.user.message_set.create(message=_("Successfully updated the affair '%s'") % affair.theme)
                return HttpResponseRedirect(reverse("affair_management", args=(affair.id,)))
        else:
            affair_form = form_class(instance=affair)
    else:
        affair_form = form_class(instance=affair)
    return render_to_response(template_name, {
        "affair_form": affair_form,
        "affair": affair,
    }, context_instance=RequestContext(request))
    
def my_affairs(request, template_name="wearetogether/my_affair.html"):
    affair_relationship = AffairRelationShip.objects.filter(partner=request.user)
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "affair_relationship":affair_relationship,
    }, context_instance=RequestContext(request))
    
def details(request,id, form_class=AffairDiaryForm, template_name="wearetogether/details.html"):
    affair = Affair.objects.filter(pk=id)
    if not affair:
        raise Http404
    else:
        affair = affair[0]
        affair_diaries = AffairDiary.objects.filter(affair_id=affair.id) 
    if request.method == "POST":
        if request.POST["action"] == "create":
            affair_diary = AffairDiary(author=request.user, affair=affair, body=request.POST['message'], tags=request.POST['tags'], 
                                       latitude=affair.latitude, longitude=affair.longitude)
            affair_diary.save()
            affair.updated_at = datetime.now()
            affair.save()
        affair_form = form_class()
    else:
        affair_form = form_class()
    print affair.theme
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "affair":affair,
        "affair_diaries":affair_diaries,
        "affair_form":affair_form,
    }, context_instance=RequestContext(request))
    
def comment(request, id, template_name="wearetogether/comment_affair_diary.html"):
    diary = get_object_or_404(AffairDiary, id=id)
    return render_to_response(template_name, {
        "diary": diary,
    }, context_instance=RequestContext(request))

def affair_diary_destroy(request, id):
    diary = AffairDiary.objects.filter(pk=int(id))
    if not diary:
        raise Http404
    else:
        diary = diary[0]
    dating_id = diary.dating_id
    if diary.author != request.user:
            request.user.message_set.create(message="You can't delete diary that aren't yours")
            return HttpResponseRedirect(reverse("affair_details", args=(dating_id,)))
    if request.method == "POST" and request.POST["action"] == "delete":
        diary.delete()
        return HttpResponseRedirect(reverse("affair_details", args=(dating_id,)))
    else:
        return HttpResponseRedirect(reverse("affair_details", args=(dating_id,)))
    return render_to_response(context_instance=RequestContext(request))

def affairship_destroy(request, id):
    affairship = AffairShip.objects.filter(dating_id=int(id), partner=request.user)   
    if not affairship:
        raise Http404
    else:
        affairship = Affairship[0]
    if request.method == "POST" and request.POST["action"] == "delete":
        affairship.delete()
        return HttpResponseRedirect(reverse("my_affairs"))
    else:
        return HttpResponseRedirect(reverse("my_affairs"))
    return render_to_response(context_instance=RequestContext(request))