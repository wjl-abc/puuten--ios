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

from wat.models import *
from wat.forms import BuzzForm, BuzzDiaryForm
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from profiles.models import Profile
from business_sina.models import *
from business_sina_weibo.models import WeiBo
from action_record.models import Action

@login_required
def buzz_map(request, template_name="wat/buzz_map.html"):
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
    }, context_instance=RequestContext(request))
    
@login_required
def new_buzz(request, form_class=BuzzForm, buzz_model = Buzz, buzzship=BuzzShip,template_name="wat/new.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            if not "longitude" in request.POST:
                return HttpResponseRedirect("/wat/new/")
            else:
                buzz = buzz_model(creator=request.user, latitude=request.POST['latitude'], longitude=request.POST['longitude'], title=request.POST['title'], tags=request.POST['tags'], body=request.POST['body'], accessing_mode=request.POST['accessing_mode'])
                buzz.save()
                if request.POST['reference_bs']:
                    buzz.reference_bs=request.POST['reference_bs']
                if request.POST['reference_wb']:
                    buzz.reference_wb=request.POST['reference_wb']
                buzz.save()
                buzzship_instance = buzzship(partner=request.user, buzz=buzz, message='', status=4)
                buzzship_instance.save()
                guest_list_str = request.POST['guest_list'].split(",")
                for guest_id in guest_list_str:
                    if guest_id:
                        user = User.objects.get(pk=guest_id)
                        buzzship_instance = buzzship(partner=user, buzz=buzz, message=request.POST['message'], status=2)
                        buzzship_instance.save()
                return HttpResponseRedirect(reverse(request.POST['dir_page']))
    bs_id = request.GET.get("bs_id", None)
    wb_id = request.GET.get("wb", None)
    dir = request.GET.get("dir", None)
    partner_id = request.GET.get("partner",None)
    buzz_form = form_class()
    if bs_id:
        buzz_form.fields['reference_bs'].initial = u"%s" % bs_id
        bs = BSInfo.objects.get(pk=bs_id)
        attachment = {"bs":bs}
    else:
        attachment = {"bs":0}
    if wb_id:
        buzz_form.fields['reference_wb'].initial = u"%s" % wb_id
        wb = WeiBo.objects.get(pk=wb_id)
        bs = BSInfo.objects.get(sina_id=wb.sina_userid)
        attachment["wb"]=wb
        attachment['bs']=bs
    else:
        attachment["wb"]=0
    if dir:
        attachment["dir"]=dir
    else:
        attachment["dir"]=0
    if partner_id:
        attachment["partner"]=User.objects.get(pk=partner_id)
    else:
        attachment["partner"]=0
    return render_to_response(template_name,{
        "profile":request.user.get_profile(),
        "buzz_form":buzz_form,
        "attachment":attachment,
    }, context_instance=RequestContext(request))
    

@login_required
def your_buzz(request, template_name='wat/your_buzz.html'):
    edit_profile_url = "/profiles/edit/"
    if not request.user.get_profile().name:
        return HttpResponseRedirect(edit_profile_url)
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "buzzship":BuzzShip.objects.filter(partner=request.user),
    }, context_instance=RequestContext(request))
    
@login_required
def details(request,id, form_class=BuzzDiaryForm, template_name="wat/details.html"):
    buzz = Buzz.objects.filter(id=id)
    if not buzz:
        raise Http404
    else:
        buzz = buzz[0]
        buzz_diaries = BuzzDiary.objects.filter(buzz_id=id) 
        wb = WeiBo.objects.get(pk=buzz.reference_wb)
        bs = BSInfo.objects.get(sina_id = wb.sina_userid)
    if request.method == "POST":
        if request.POST["action"] == "create":
            buzz_diary = BuzzDiary(author=request.user, buzz=buzz, body=request.POST['message'])
            buzz_diary.save()
            actions = Action.objects.filter(object_type=ContentType.objects.get(model=buzz.get_type()), object_id=buzz.id, performer=request.user, act=2)
            if actions.count() > 0:
                action = actions[0]
                action.time = datetime.now
                action.save()
            else:
                action = Action(performer=request.user, act=2, object=buzz)
                action.save()
        diary_form = form_class()
    else:
        diary_form = form_class()
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "buzz":buzz,
        "wb":wb,
        "bs":bs,
        "buzz_diaries":buzz_diaries,
        "diary_form":diary_form,
    }, context_instance=RequestContext(request))
    
@login_required
def diary_destroy(request, id):
    diary = BuzzDiary.objects.filter(buzz_id=int(id))
    if not diary:
        raise Http404
    else:
        diary = diary[0]
    buzz_id = diary.buzz_id
    if diary.author != request.user:
            request.user.message_set.create(message="You can't delete diary that aren't yours")
            return HttpResponseRedirect(reverse("dating_details", args=(buzz_id,)))
    if request.method == "POST" and request.POST["action"] == "delete":
        diary.delete()
        return HttpResponseRedirect(reverse("buzz_details", args=(buzz_id,)))
    else:
        return HttpResponseRedirect(reverse("buzz_details", args=(buzz_id,)))
    return render_to_response(context_instance=RequestContext(request))

@login_required
def buzzship_destroy(request, id):
    buzzship = BuzzShip.objects.filter(buzz_id=int(id), partner=request.user)   
    if not buzzship:
        raise Http404
    else:
        buzzship = buzzship[0]
    if request.method == "POST" and request.POST["action"] == "delete":
        buzzship.delete()
        return HttpResponseRedirect(reverse("your_buzz"))
    else:
        return HttpResponseRedirect(reverse("your_buzz"))
    return render_to_response(context_instance=RequestContext(request))

@login_required
def comment(request, id, template_name="ijustdated/comment_diary.html"):
    diary = get_object_or_404(BuzzDiary, id=id)
    return render_to_response(template_name, {
        "diary": diary,
    }, context_instance=RequestContext(request))
    
@login_required
def edit(request, id, form_class=BuzzForm, template_name="wat/edit.html"):
    buzz = get_object_or_404(Buzz, id=id)
    if request.method == "POST":
        if buzz.creator != request.user:
            request.user.message_set.create(message="You can't edit buzz that aren't yours")
            return HttpResponseRedirect(reverse("your_buzz"))
        if request.POST["action"] == "update":
            buzz_form = form_class(request.user, request.POST, instance=buzz)
            if buzz_form.is_valid():
                buzz = buzz_form.save(commit=False)
                buzz.save()
                request.user.message_set.create(message=_("Successfully updated post '%s'") % buzz.title)
                return HttpResponseRedirect(reverse("your_buzz"))
        else:
            buzz_form = form_class(instance=buzz)
    else:
        buzz_form = form_class(instance=buzz)
    return render_to_response(template_name, {
        "buzz_form": buzz_form,
        "buzz": buzz,
    }, context_instance=RequestContext(request))
    
def admin(request, id, template_name="wat/admin.html"):
    buzz = Buzz.objects.get(pk=id)
    buzz_members = []
    applications = []
    approved_buzzship_list = BuzzShip.objects.filter(buzz_id=id, status=4).exclude(partner=buzz.creator)
    pending_buzzship_list  = BuzzShip.objects.filter(buzz_id=id, status=2)
    buzz_member_id         = request.POST.get("buzz_member_id", None)
    applicant_id           = request.POST.get("applicant_id", None)
    if buzz.creator==request.user:
        is_creator = True
    else:
        is_creator = False
    for instance in approved_buzzship_list:
        buzz_members.append(instance.partner)
    for instance in pending_buzzship_list:
        applications.append(instance.partner)
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
        if request.POST['action']=='invite':
            return HttpResponseRedirect(reverse("buzz_admin", args=(id,)))
        elif request.POST['action']=='join':
            if buzz.accessing_mode == 3:
                buzz_ship = BuzzShip(buzz=buzz, partner=request.user, message="", status=2)
                buzz_ship.save()
            elif buzz.accessing_mode == 1:
                buzz_ship = BuzzShip(buzz=buzz, partner=request.user, message="", status=4)
                buzz_ship.save()
            return HttpResponseRedirect(reverse("buzz_admin", args=(id,)))
        elif request.POST['action']=='remove':
            partner = User.objects.get(pk=buzz_member_id)
            buzz_ship = BuzzShip.objects.filter(buzz_id=id, partner=partner, status=4)
            for instance in buzz_ship:
                instance.delete()
            return HttpResponseRedirect(reverse("buzz_admin", args=(id,)))
        elif request.POST['action']=='approve':
            partner = User.objects.get(pk=applicant_id)
            buzz_ship = BuzzShip.objects.filter(buzz_id=id, partner=partner, status=2)
            for instance in buzz_ship:
                instance.status=4
                instance.save()
            return HttpResponseRedirect(reverse("buzz_admin", args=(id,)))
        elif request.POST['action']=='reject':
            partner = User.objects.get(pk=applicant_id)
            buzz_ship = BuzzShip.objects.filter(buzz_id=id, partner=partner, status=2)
            for instance in buzz_ship:
                instance.delete()
            return HttpResponseRedirect(reverse("buzz_admin", args=(id,)))
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "buzz":buzz,
        "applications":applications,
        "buzz_members":buzz_members,
        "related_or_not":BuzzShip.objects.filter(buzz_id=id, partner=request.user),
        "is_creator":is_creator,
    }, context_instance=RequestContext(request))
