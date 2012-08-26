#coding=utf-8
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from geo_info.models import *
from geo_info.forms import *

@login_required    
def info(request, form_class=GeoInfoForm, geo_info_class=GeoInfo, template_name="geo/geo_info.html"):
    geo_info_list = GeoInfo.objects.all()
    if request.method == "POST":
        if request.POST["action"] == "create":
            instance = GeoInfo.objects.filter(city=request.POST['city'])
            if instance:
                request.user.message_set.create(message="This info is in the system already.")
                return HttpResponseRedirect(reverse("geo_info"))
            else:
                geo_info = geo_info_class(city=request.POST['city'], lat=request.POST['lat'], lng=request.POST['lng'])
                geo_info.save()
                return HttpResponseRedirect(reverse("geo_info"))
    else:
        geo_info_form = form_class()
    return render_to_response(template_name, { 
        "geo_info_list":geo_info_list,
        "geo_info_form":geo_info_form,
    }, context_instance=RequestContext(request))
    
@login_required    
def geo_info_destroy(request, id):
    geo_info = GeoInfo.objects.get(pk=id)
    if request.user.id != 1:
        request.user.message_set.create(message="You can't delete this geo info")
        return HttpResponseRedirect(reverse("geo_info"))

    if request.method == "POST" and request.POST["action"] == "delete":
        geo_info.delete()
        return HttpResponseRedirect(reverse("geo_info"))
    else:
        return HttpResponseRedirect(reverse("geo_info"))

    return render_to_response(context_instance=RequestContext(request))
