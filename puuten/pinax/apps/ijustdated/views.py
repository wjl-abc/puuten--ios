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

from ijustdated.models import *
from ijustdated.forms import DatingForm, DatingDiaryForm
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from profiles.models import Profile
from wishing_list.models import *
from business_sina.models import *
from business_sina_weibo.models import WeiBo

def dating_map(request, template_name="ijustdated/dating_map.html"):
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "datings":Dating.objects.all()
    }, context_instance=RequestContext(request))

@login_required
def new_dating(request, form_class=DatingForm, dating_model = Dating, datingship=DatingShip,template_name="ijustdated/new_dating.html"):
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
            if not "longitude" in request.POST:
                return HttpResponseRedirect("/ijustdated/new/")
            else:
                dating_form = form_class(request.user, request.POST)
                dating = dating_model(creator=request.user, latitude=request.POST['latitude'], longitude=request.POST['longitude'], tags=request.POST['tags'])
                dating.save()
                if request.POST['items']=='mf':
                    dating.dating_mode=2
                elif request.POST['items']=='mm':
                    dating.dating_mode=1
                else:
                    dating.dating_mode=3
                if request.POST['reference_bs']:
                    dating.reference_bs=request.POST['reference_bs']
                if request.POST['reference_wb']:
                    dating.reference_wb=request.POST['reference_wb']
                dating.save()
                if "dating_partner" in request.POST:
                    partner = User.objects.get(pk=request.POST['dating_partner'])
                else:
                    default_partnership=DefaultPartnerShip.objects.filter(default_from_user=request.user, default_status=1)
                    partner = default_partnership[0].default_to_user
                datingship_instance = datingship(partner=request.user, dating_type=ContentType.objects.get(model=dating.get_type()), dating_id=dating.id, message=request.POST['message'], status=4)
                datingship_instance.save()
                #default_accept_or_not = DefaultPartnerShip(default_from_user=partner, default_to_user=request.user, default_status=2)
                #if default_accept_or_not:
                #    datingship_instance = datingship(partner=partner, dating_type=ContentType.objects.get(model=dating.get_type()), dating_id=dating.id, message="", status=4)
                #else:
                datingship_instance = datingship(partner=partner, dating_type=ContentType.objects.get(model=dating.get_type()), dating_id=dating.id, message=request.POST['message'], status=2)
                datingship_instance.save()
                if "default_setting" in request.POST:
                    default_partnership=DefaultPartnerShip.objects.filter(default_from_user=request.user, default_status=1)
                    if default_partnership:
                        default_partnership[0].delete()
                    default_partnership = DefaultPartnerShip(default_from_user=request.user, default_to_user=partner, default_status=1)
                    default_partnership.save()
                return HttpResponseRedirect(reverse("dating_details", args=(dating.id,))) 
                
    default_partnership = DefaultPartnerShip.objects.filter(default_from_user=request.user, default_status=1)
    dating_form=form_class()
    if default_partnership:
        attachment = {"flag":1, "default_partner":default_partnership[0].default_to_user}
    else:
        attachment = {"flag":0, "default_partner":0}
    bs_id = request.GET.get("bs_id", None)
    wb_id = request.GET.get("wb", None)
    partner_id = request.GET.get("partner_id", None)
    if bs_id:
        dating_form.fields['reference_bs'].initial = u"%s" % bs_id
        bs = BSInfo.objects.get(pk=bs_id)
        attachment["bs"]=bs
    else:
        attachment["bs"]=0
    if wb_id:
        dating_form.fields['reference_wb'].initial = u"%s" % wb_id
        wb = WeiBo.objects.get(pk=wb_id)
        attachment["wb"]=wb
    else:
        attachment["wb"]=0
    if partner_id:
        partner = User.objects.get(pk=partner_id)
        attachment["partner"]=partner
        attachment["default_partner"]=0
        attachment["flag"]=1
    else:
        attachment["partner"]=0
    return render_to_response(template_name,{
        "profile":request.user.get_profile(),
        "dating_form":dating_form,
        "attachment":attachment,
    }, context_instance=RequestContext(request))
    
def my_dating(request, template_name='ijustdated/my_dating.html'):
    edit_profile_url = "/profiles/edit/"
    if not request.user.get_profile().name:
        return HttpResponseRedirect(edit_profile_url)
    if request.method == "POST":
        datingship_id = request.POST.get("datingship", None)
        if request.POST["action"] == "datingship_accept":
            datingship = DatingShip.objects.get(id=datingship_id)
            datingship.status=4
            datingship.save()
            if "default_setting" in request.POST:
                default_partnership = DefaultPartnerShip(default_from_user=request.user, default_to_user=datingship.dating.creator, default_status=2)
                default_partnership.save()
        elif request.POST["action"] == "datingship_reject":
            datingship = DatingShip.objects.get(id=datingship_id)
            datingship.status=5
            datingship.save()
    datings = DatingShip.objects.filter(partner=request.user, status=2)
    for instance in datings:
        print instance.dating.tags
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "dating_ship_approved":DatingShip.objects.filter(partner=request.user, status=4),
        "dating_ship_pending":DatingShip.objects.filter(partner=request.user, status=2),
    }, context_instance=RequestContext(request))
    
def details(request,id, form_class=DatingDiaryForm, template_name="ijustdated/details.html"):
    dating = Dating.objects.filter(id=id)
    partner = []
    if not dating:
        raise Http404
    else:
        dating = dating[0]
        if dating.reference_bs:
            bs = BSInfo.objects.get(pk=dating.reference_bs)
        else:
            bs = 0
        if dating.reference_wb:
            wb = WeiBo.objects.get(pk=dating.reference_wb)
        else:
            wb = 0
        datingship = DatingShip.objects.filter(dating_id=dating.id)
        if len(datingship)>1:
            if datingship[0].dating==dating:
                dating_ship = datingship[1]
            else:
                dating_ship = datingship[0]
            partner = dating_ship.partner
        dating_diaries = DatingDiary.objects.filter(dating_id=dating.id) 
    if request.method == "POST":
        if request.POST["action"] == "create":
            dating_diary = DatingDiary(author=request.user, dating=dating, body=request.POST['message'], tags=request.POST['tags'], 
                                       latitude=dating.latitude, longitude=dating.longitude)
            dating_diary.save()
            dating.updated_at = datetime.now()
            dating.save()
        diary_form = form_class()
        if request.POST["action"] == "submit":
            wish_list_int = []
            #wishing_list_wish = []
            wish_list_str = request.POST['name'].split(",")
            for wish_id in wish_list_str:
                if wish_id:
                    wish_list_int.append(int(wish_id))
            print wish_list_int
            for wish_id in wish_list_int:
                wish = Wish.objects.get(pk=wish_id)
                if request.user==wish.owner:
                    wish_realize = Wish_Realize(wish=wish, realized=dating, status=2)
                    wish_realize.save()
                else:
                    wish_realize = Wish_Realize(wish=wish, realized=dating, status=1)
                    wish_realize.save()
    else:
        dating = Dating.objects.filter(id=id)
        partner = []
        if not dating:
            raise Http404
        else:
            dating = dating[0]
            if dating.reference_bs:
                bs = BSInfo.objects.get(pk=dating.reference_bs)
            else:
                bs = 0
            if dating.reference_wb:
                wb = WeiBo.objects.get(pk=dating.reference_wb)
            else:
                wb = 0
            datingship = DatingShip.objects.filter(dating_id=dating.id)
            if len(datingship)>1:
                if datingship[0].dating==dating:
                    dating_ship = datingship[1]
                else:
                    dating_ship = datingship[0]
                partner = dating_ship.partner
            dating_diaries = DatingDiary.objects.filter(dating_id=dating.id) 
        diary_form = form_class()
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "dating":dating,
        "bs":bs,
        "wb":wb,
        "dating_diaries":dating_diaries,
        "diary_form":diary_form,
        "partner":partner,
    }, context_instance=RequestContext(request))
    
def diary_destroy(request, id):
    diary = DatingDiary.objects.filter(pk=int(id))
    if not diary:
        raise Http404
    else:
        diary = diary[0]
    dating_id = diary.dating_id
    if diary.author != request.user:
            request.user.message_set.create(message="You can't delete diary that aren't yours")
            return HttpResponseRedirect(reverse("dating_details", args=(dating_id,)))
    if request.method == "POST" and request.POST["action"] == "delete":
        diary.delete()
        return HttpResponseRedirect(reverse("dating_details", args=(dating_id,)))
    else:
        return HttpResponseRedirect(reverse("dating_details", args=(dating_id,)))
    return render_to_response(context_instance=RequestContext(request))

def datingship_destroy(request, id):
    datingship = DatingShip.objects.filter(dating_id=int(id), partner=request.user)   
    if not datingship:
        raise Http404
    else:
        datingship = datingship[0]
    if request.method == "POST" and request.POST["action"] == "delete":
        datingship.delete()
        return HttpResponseRedirect(reverse("my_dating"))
    else:
        return HttpResponseRedirect(reverse("my_dating"))
    return render_to_response(context_instance=RequestContext(request))

def comment(request, id, template_name="ijustdated/comment_diary.html"):
    diary = get_object_or_404(DatingDiary, id=id)
    return render_to_response(template_name, {
        "diary": diary,
    }, context_instance=RequestContext(request))
