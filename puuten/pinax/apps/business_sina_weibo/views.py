# -*- coding: utf-8 -*- 
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
import sys
from business_sina.models import *
from business_sina_weibo.models import *
from business_sina.forms import BSInfoForm
from social_auth.views import delete_BSInfo_Friendships
from wishing_list.models import Wish
from tagging.models import Tag, TaggedItem
from action_record.models import Action
from wat.models import Buzz, BuzzShip

@login_required
def bs_weibo_list(request, bs_id, template_name="business_sina_weibo/bs_weibolist.html"):
    bs = BSInfo.objects.get(pk=bs_id)
    if request.method == "POST":
        if "mobile" in request.POST:
            print "test successful"
            data = json.dumps({"name":bs.name, "avatar_url":bs.avatar, "tags":bs.tags, "introduction":bs.introduction})
            return HttpResponse(mark_safe(data))
        if request.POST["action"] == "create":
            buzz = Buzz(creator=request.user)
            buzz.save()
            if request.POST['reference_bs']:
                buzz.reference_bs=request.POST['reference_bs']
            if request.POST['reference_wb']:
                buzz.reference_wb=request.POST['reference_wb']
            buzz.save()
            buzzship_instance = BuzzShip(partner=request.user, buzz=buzz, message='', status=4)
            buzzship_instance.save()
            guest_list_str = request.POST['guest_list'].split(",")
            for guest_id in guest_list_str:
                if guest_id:
                    user = User.objects.get(pk=guest_id)
                    buzzship_instance = BuzzShip(partner=user, buzz=buzz, message=request.POST['body'], status=2)
                    buzzship_instance.save()
        if request.POST["action"] == "add_wish":
            wb = WeiBo.objects.get(pk = request.POST['id'])
            new_wish = Wish(owner=request.user, shared=wb, tags="wishing_list")
            new_wish.save()
            action = Action(performer=request.user, act=1, object=new_wish)
            action.save()
    if bs.new_name is not None:
        bs.name = bs.new_name
    weibolist = WeiBo.objects.filter(sina_userid=bs.sina_id)
    for weibo in weibolist:
        weibo.sina_user = bs
        
    return render_to_response(template_name, {
        "weibolist": weibolist,
        "bs":bs,
    }, context_instance=RequestContext(request))

def update_WeiBo_Status(ids,status):    
    for rid in ids.split(','):
        if rid== "" :
            continue;
        try:
            wb = WeiBo.objects.get(sina_id=rid)
            wb.status = status
            wb.save()
        except:
            print "Unexpected error:", sys.exc_info()  
            
def change_date_format(date):
    date=date.split("/")
    year = int(date[2])
    month = int(date[0])
    day  = int(date[1])
    return datetime(year, month, day)
    

@login_required
def bs_all_new_weibo_list(request, model=InfoDisplay, template_name="business_sina_weibo/bs_allweibolist.html"):
    #1,4,均属于管理员没检查的记录
    result = BSAdmin.objects.filter(b_s_admin=request.user)
    if result:
        bs_admin_or_not=True
    else:
        bs_admin_or_not=False
    if request.method == "POST":
        if request.POST["action"] == "submit":
            display_from = request.POST['from'].split(",")
            display_to   = request.POST['to'].split(',')
            id_list      = request.POST['wb_id'].split(',')
            checked_list = request.POST['checked_id'].split(',')
            tags_list    = request.POST['tags'].split(',')
            for i in range(0,len(display_from)-1):
                wb= WeiBo.objects.get(pk=int(id_list[i]))
                owner= BSInfo.objects.get(sina_id=wb.sina_userid)
                info_display = model(info_owner=owner, latitude=owner.latitude, longitude=owner.longitude, info=wb, begin=change_date_format(display_from[i]), end=change_date_format(display_to[i]), tags=tags_list[i], created_by=request.user)
                info_display.save()
                wb.status='2'
                wb.save()
            for i in range(0, len(checked_list)-1):
                wb=WeiBo.objects.get(pk=int(checked_list[i]))
                wb.status='3'
                wb.save()       
#    bss = []
#    for bs in BSInfo.objects.filter(status=1):
#        bss.append(bs.sina_id)  
#    weibolist = WeiBo.objects.filter(sina_userid__in = bss, status ='4' ).order_by('sina_id')
    weibolist = []
    bss = []
    bs_list = BSInfo.objects.all()
    for instance in bs_list:
        bss.append(instance.sina_id)
    weibo_list_temp = WeiBo.objects.filter(status ='5' ).order_by('sina_id')
    for instance in weibo_list_temp:
        if instance.sina_userid in bss:
            weibolist.append(instance)

    for weibo in weibolist:
        bs = BSInfo.objects.get(sina_id = weibo.sina_userid)
        if bs.new_name is not None:
            bs.name = bs.new_name
        weibo.sina_user = bs
    return render_to_response(template_name, {
        "weibolist": weibolist,
        "bs_admin_or_not": bs_admin_or_not,
    }, context_instance=RequestContext(request))
    
@login_required
def weibo(request, id, template_name="business_sina_weibo/weibo.html"):
    wb = WeiBo.objects.get(pk=id)
    if request.method == "POST":
        if "mobile" in request.POST:
            bs = BSInfo.objects.get(sina_id=wb.sina_userid) 
            data = json.dumps({"name":wb.get_owner_name(), "body":wb.sina_text, "avatar_url":bs.avatar, "bs_id":bs.id})
            return HttpResponse(mark_safe(data))
    return render_to_response(template_name, {
        "wb":wb,
    },context_instance=RequestContext(request))

    
def add_2_wishing_list(request, wb_id, wish_model=Wish):
    wb = WeiBo.objects.get(pk=wb_id)
    if request.method == "POST":
        if request.POST["action"] == "add_to_my_wishing_list":
            if Wish.objects.filter(shared_type=ContentType.objects.get(model=wb.get_type()), shared_id=wb_id, owner=request.user, tags="wishing_list").count() > 0:
                request.user.message_set.create(message="You had ready added it to your wishing list.")
            else:
                new_wish = wish_model(owner=request.user, shared=wb, content_type=3, tags="wishing_list")
                new_wish.save()
                return HttpResponseRedirect(reverse("your_wishing_list"))

@login_required
def recommendation_del(request, id):
    result = BSAdmin.objects.filter(b_s_admin=request.user)
    wb = WeiBo.objects.get(pk=id)
    if not result:
        request.user.message_set.create(message="You can't delete this WeiBo")
        return HttpResponseRedirect(reverse("bs_all_new_weibo_list"))
    if request.method == "POST" and request.POST["action"] == "delete":
        wb.delete()
        request.user.message_set.create(message="You successfully deleted this WeiBo")
        return HttpResponseRedirect(reverse("bs_all_new_weibo_list"))
    else:
        return HttpResponseRedirect(reverse("bs_all_new_weibo_list"))
    return render_to_response(context_instance=RequestContext(request))

@login_required
def wb_comments(request, id, template_name="business_sina_weibo/weibo_comments.html"):
    wb = get_object_or_404(WeiBo, id=id)
    next = request.GET.get("next", None)
    return render_to_response(template_name, {
        "wb": wb,
        "next": next
    }, context_instance=RequestContext(request))