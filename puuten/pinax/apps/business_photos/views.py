#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.db.models import Q
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from photologue.models import *
from photos.models import Image, Pool
from photos.forms import PhotoUploadForm, PhotoEditForm
from share.models import Share
from share.forms import *
from wishing_list.models import Wish
from business_photos.models import BusinessImage
from business_photos.forms import BusinessPhotoUploadForm, BusinessPhotoEditForm
from business.models import *
from business_blog.models import *

#add by jipan
from django.utils.translation import gettext
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils import simplejson as json
import uuid
import sys

@login_required
def keditorupload(request, business_id, form_class=BusinessPhotoUploadForm,
        template_name="business_photos/upload.html", group_slug=None, bridge=None):
    """
    upload form for photos
    """    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    photo_form = form_class()
    surl = ''
    error = 1
    message = ''
    business = BusinessProfile.objects.get(pk=business_id)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    
    try:        
        if not is_manager:
            raise  "没有管理权限"
    
        if request.method == 'POST' :
            request.POST['title'] = uuid.uuid1().__str__()
            request.POST['safetylevel'] = '1'#Image.SAFETY_LEVEL 
            request.POST["latitude"] = business.latitude
            request.POST["longitude"] = business.longitude
            print request.POST
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.owner_type = 2
                photo.owner_id = business_id
                photo.latitude = business.latitude
                photo.longitude = business.longitude
                photo.save()
                error = 0
                surl = photo.get_display_url()
                message = gettext('Successfully uploaded photo')     
            # in group context we create a Pool object for it
                if group:
                    pool = Pool()
                    pool.photo = photo
                    group.associate(pool)
                    pool.save()
    except:
        print "Unexpected error:", sys.exc_info()
        error = 1
        message=gettext("Uploaded photo faild")
    json_response_data = {"error":error, "url":surl, "message":message}
    print json_response_data
    return HttpResponse(mark_safe(json.encode(json_response_data)))

@login_required
def new(request, business_id, form_class=BusinessPhotoUploadForm,
        template_name="business_photos/upload.html", group_slug=None, bridge=None):
    """
    upload form for photos
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.owner_type = 2
                photo.owner_id = business_id
                photo.latitude = business.latitude
                photo.longitude = business.longitude
                photo.save()
                 
                # in group context we create a Pool object for it
                if group:
                    pool = Pool()
                    pool.photo = photo
                    group.associate(pool)
                    pool.save()
                
                request.user.message_set.create(message=_("Successfully uploaded photo '%s'") % photo.title)
                
                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("business_blogs", args=business_id)
                return HttpResponseRedirect(redirect_to)
        else:
            photo_form = form_class()
    else:
        photo_form = form_class()
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "is_manager":is_manager,
        "group": group,
        "photo_form": photo_form,
    }, context_instance=RequestContext(request))

@login_required     
def photos(request, business_id, template_name="business_photos/photos.html", group_slug=None, bridge=None):
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    photos = BusinessImage.objects.filter(owner_id=business_id, owner_type=2)
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "is_manager":is_manager,
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))

@login_required     
def photo(request, business_id, photo_id, wish_model = Wish, group_slug=None, bridge=None, template_name="business_photos/photo.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
        
    photos = BusinessImage.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=photo_id)
    
    if not photo.is_public and request.user != photo.member:
        raise Http404
    
    photo_url = photo.get_display_url()
    
    title = photo.title
    host = "http://%s" % get_host(request)
    
    image = BusinessImage.objects.get(pk=photo_id)
    if request.method == "POST":
        if request.POST["action"] == "add_to_my_wishing_list":
            if Wish.objects.filter(shared_type=ContentType.objects.get(model=blog_instance.get_type()), shared_id=blog_instance.id).count() > 0:
                request.user.message_set.create(message="You had ready added it to your wishing list.")
            else:
                new_wish = wish_model(owner=request.user, shared=blog_instance, tags="wishing_list", content_type=2)
                new_wish.save()
                return HttpResponseRedirect(reverse("your_wishing_list"))
    return render_to_response(template_name, {
        "group": group,
        "host": host,
        "business":business,
        "business_app_list":business_app_list,
        "photo":photo,
        "photo_url": photo_url,
        "is_manager":is_manager,
    },context_instance=RequestContext(request))

@login_required     
def edit(request, business_id, photo_id, form_class=BusinessPhotoEditForm, template_name="business_photos/edit.html", group_slug=None, bridge=None):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = BusinessImage.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=photo_id)
    photo_url = photo.get_display_url()
    
    if request.method == "POST":
        if not is_manager:
            request.user.message_set.create(message="You can't edit this photo.")
            return HttpResponseRedirect(photo.get_absolute_url())
        if request.POST["action"] == "update":
            photo_form = form_class(request.user, request.POST, instance=photo)
            if photo_form.is_valid():
                photoobj = photo_form.save(commit=False)
                photoobj.save()
                
                request.user.message_set.create(message=_("Successfully updated photo '%s'") % photo.title)
                
                return HttpResponseRedirect(photo.get_absolute_url())
        else:
            photo_form = form_class(instance=photo)
    else:
        photo_form = form_class(instance=photo)
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "is_manager":is_manager,
        "group": group,
        "photo_form": photo_form,
        "photo": photo,
        "photo_url": photo_url,
    }, context_instance=RequestContext(request))
    
def destroy(request, business_id, photo_id, group_slug=None, bridge=None):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = BusinessImage.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=photo_id)
    title = photo.title
    
    if is_manager:
        if request.method == "POST" and request.POST["action"] == "delete":
            photo.delete()
            request.user.message_set.create(message=_("Successfully deleted photo '%s'") % title)
            return HttpResponseRedirect(reverse("business_photos", args=business_id))
        else:
            return HttpResponseRedirect(reverse("business_photos", args=business_id))
    else:
        request.user.message_set.create(message="You can't delete this photo")
        return HttpResponseRedirect(reverse("business_photos", args=business_id))
