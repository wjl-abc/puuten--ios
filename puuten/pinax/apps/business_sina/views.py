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

from business_sina.models import *
from business_sina.forms import BSInfoForm
from social_auth.views import delete_BSInfo_Friendships

def bs_new(request, form_class=BSInfoForm, template_name="business_sina/new.html"):
    profile = request.user.get_profile()
    result = BSAdmin.objects.filter(b_s_admin=request.user)
    if result:
        bs_admin_or_not=True
    else:
        bs_admin_or_not=False
    if request.method == "POST":
        if request.POST["action"] == "create":
            business_sina_form = form_class(request.user, request.POST)
            if business_sina_form.is_valid():
                business_sina = business_sina_form.save(commit=False)
                business_sina.created_by = request.user
                business_sina.status = "2"
                business_sina.save()
                return HttpResponseRedirect(reverse("your_collection"))
    business_sina_form=form_class()
    return render_to_response(template_name, {
        "profile":profile,
        "bs_admin_or_not": bs_admin_or_not,
        "business_sina_form":business_sina_form,
    }, context_instance=RequestContext(request))

def bs_location(request, template_name="business_sina/bs_location.html"):
    profile = request.user.get_profile()
    result = BSAdmin.objects.filter(b_s_admin=request.user)
    if result:
        bs_admin_or_not=True
    else:
        bs_admin_or_not=False
    business_list = BSInfo.objects.filter(status=2)
    if len(business_list)>=300:
        business_list = business_list[0:300]
    business_count = len(business_list)
    if request.method == "POST":
        if request.POST["action"] == "submit":
            lat_list_float = []
            lng_list_float = []
            id_list_int = []
            lat_list_str = request.POST['lat'].split(",")
            lng_list_str = request.POST['lng'].split(",")
            id_list_str = request.POST['business_id'].split(",")
            list_length = len(lat_list_str)-1
            for i in range(0, list_length):
                lat_list_float.append(float(lat_list_str[i]))
            for i in range(0, list_length):
                lng_list_float.append(float(lng_list_str[i]))
            for i in range(0, list_length):
                id_list_int.append(int(id_list_str[i]))
            for i in range(0, list_length):
                if lat_list_float[i]<500:
                    business = BSInfo.objects.get(pk=id_list_int[i])
                    business.latitude=lat_list_float[i]
                    business.longitude=lng_list_float[i]
                    business.status=1
                    business.save()
                else:
                    business = BSInfo.objects.get(pk=id_list_int[i])
                    if business.status==2:
                        business.latitude = 500.1
                        business.longitude = 500.1
                        business.status=3
                        business.save()   
        return HttpResponseRedirect(reverse("your_collection"))
    return render_to_response(template_name, {
        "profile":profile,
        "bs_admin_or_not": bs_admin_or_not,
        "business_list_sorted":business_list,
        "business_count":business_count,
    }, context_instance=RequestContext(request))
    
def bs_edit(request, id, template_name="business_sina/edit.html"):
    bs = BSInfo.objects.get(pk=id)
    is_manager = BSAdmin.objects.get(b_s_admin=request.user)
    if is_manager:
        if request.method == "POST" and request.POST["action"] == "submit":
            if float(request.POST['lat'])<500:
                bs.latitude=float(request.POST['lat'])
                bs.longitude=float(request.POST['lng'])
                if request.POST['new_name']:
                    bs.new_name=request.POST['new_name']
                bs.created_by=request.user
                bs.updated_at=datetime.now()
                bs.status=1
                bs.save()
            return HttpResponseRedirect(reverse("your_collection"))
    else:
        request.user.message_set.create(message="You can't edit this business information")
        return HttpResponseRedirect(reverse("your_collection"))
    return render_to_response(template_name, {
        "is_manager": is_manager,
        "business_from_sina":bs,
    }, context_instance=RequestContext(request))
def bs_del(request, id):
    bs = BSInfo.objects.get(pk=id)
    name = bs.name
    is_manager = BSAdmin.objects.get(b_s_admin=request.user)
    if is_manager:
        if request.method == "POST" and request.POST["action"] == "delete":
            delete_BSInfo_Friendships(BSInfo_sinaid=bs.sina_id, BSInfo_followed_by_id=bs.followed_by_id)
            bs.delete()
            request.user.message_set.create(message=_("Successfully deleted business '%s'") % name)
            return HttpResponseRedirect(reverse("your_collection"))
        else:
            return HttpResponseRedirect(reverse("your_collection"))
    else:
        request.user.message_set.create(message="You can't delete this business")
        return HttpResponseRedirect(reverse("your_collection"))
    
