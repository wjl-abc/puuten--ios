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
from threadedcomments.templatetags.threadedcommentstags import get_comments_count, update_animation 

#add by jipan
from django.utils.translation import gettext
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils import simplejson as json
import uuid
import sys
@login_required
def keditorupload(request, form_class=PhotoUploadForm,
        template_name="photos/upload.html", group_slug=None, bridge=None):
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
              
    try:
        if request.method == 'POST':
            request.POST['title'] = uuid.uuid1().__str__()
            request.POST['safetylevel'] = 1 #Image.SAFETY_LEVEL 
            profile = request.user.get_profile()
            request.POST["latitude"] = profile.latitude
            request.POST["longitude"] = profile.longitude
            print request.POST
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.is_public = True
                photo.owner_type = 1
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
        """
                request.user.message_set.create(message=_("Successfully uploaded photo '%s'") % photo.title)
                
                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("photo_details", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)
        """ 

    json_response_data = {"error":error, "url":surl, "message":message}
    print json_response_data
    return HttpResponse(mark_safe(json.encode(json_response_data)))


@login_required
def upload(request, form_class=PhotoUploadForm,
        template_name="photos/upload.html", group_slug=None, bridge=None):
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
    
    profile = request.user.get_profile()
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.owner_type = 1
                if request.POST["owner_id"]:
                    photo.owner_type = 2
                    photo.owner_id = int(request.POST["owner_id"])
                    business = BusinessProfile.objects.get(pk = photo.owner_id)
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
                if request.POST["owner_id"]:
                    return HttpResponseRedirect(reverse("single_business", args=(int(request.POST["owner_id"]),)))
                else:
                    if group:
                        redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
                    else:
                        redirect_to = reverse("photo_details", kwargs=include_kwargs)
                
                    return HttpResponseRedirect(redirect_to)
            if request.POST["owner_id"]:
                something = int(request.POST["owner_id"])
            else:
                something = None
        else:
            photo_form = form_class()
            something = request.GET.get("something", None)
            if something:
                photo_form.fields['owner_id'].initial = u"%s" % something
    else:
        photo_form = form_class()
        something = request.GET.get("something", None)
        if something:
            photo_form.fields['owner_id'].initial = u"%s" % something  
    return render_to_response(template_name, {
        "group": group,
        "profile": profile,
        "photo_form": photo_form,
        "something": something,
    }, context_instance=RequestContext(request))



@login_required
def yourphotos(request, username=None, template_name="photos/yourphotos.html", group_slug=None, bridge=None):
    """
    photos for the currently authenticated user
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.filter(member=request.user, owner_type=1)
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "profile":request.user.get_profile(),
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def latest(request, template_name="photos/latest.html", group_slug=None, bridge=None):
    """
    latest photos
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.filter(
        Q(is_public=True) |
        Q(is_public=False, member=request.user)
    )
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def details(request, id, template_name="photos/details.html", group_slug=None, bridge=None, share_model = Share):
    """
    show the photo details
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    
    # @@@: test
    if not photo.is_public and request.user != photo.member:
        raise Http404
    
    photo_url = photo.get_display_url()
    
    title = photo.title
    host = "http://%s" % get_host(request)
    
    if photo.member == request.user:
        is_me = True
    else:
        is_me = False
    #is_me = True
    if request.method == "POST":
        if request.POST["action"] == "share":
            if Share.objects.filter(shared_type=ContentType.objects.get(model='image'), shared_id=photo.id).count() > 0:
                request.user.message_set.create(message="You have already shared this photo")
            else:
                new_share = share_model(owner=request.user, shared=photo, content_type=2)
                new_share.save()
                update_animation(photo, 2 , 3)
                return HttpResponseRedirect(reverse("your_share"))
    return render_to_response(template_name, {
        "group": group,
        "host": host,
        "photo": photo,
        "photo_url": photo_url,
        "is_me": is_me,
    }, context_instance=RequestContext(request))


@login_required
def memberphotos(request, id, template_name="photos/memberphotos.html", group_slug=None, bridge=None):
    """
    Get the members photos and display them
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    user = get_object_or_404(User, id=id)
    
    photos = Image.objects.filter(
        member__username = user.username,
        is_public = True,
        owner_type=1,
    )
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=PhotoEditForm,
        template_name="photos/edit.html", group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    photo_url = photo.get_display_url()

    if request.method == "POST":
        if photo.member != request.user:
            request.user.message_set.create(message="You can't edit photos that aren't yours")
            
            include_kwargs = {"id": photo.id}
            if group:
                redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
            else:
                redirect_to = reverse("photo_details", kwargs=include_kwargs)
            
            return HttpResponseRedirect(reverse('photo_details', args=(photo.id,)))
        if request.POST["action"] == "update":
            photo_form = form_class(request.user, request.POST, instance=photo)
            if photo_form.is_valid():
                photoobj = photo_form.save(commit=False)
                photoobj.save()
                
                request.user.message_set.create(message=_("Successfully updated photo '%s'") % photo.title)
                
                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("photo_details", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)
        else:
            photo_form = form_class(instance=photo)

    else:
        photo_form = form_class(instance=photo)

    return render_to_response(template_name, {
        "group": group,
        "photo_form": photo_form,
        "photo": photo,
        "photo_url": photo_url,
    }, context_instance=RequestContext(request))

@login_required
def destroy(request, id, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    title = photo.title
    
    if group:
        redirect_to = bridge.reverse("photos_yours", group)
    else:
        redirect_to = reverse("photos_yours")
    
    if photo.member != request.user:
        request.user.message_set.create(message="You can't delete photos that aren't yours")
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST" and request.POST["action"] == "delete":
        photo.delete()
        request.user.message_set.create(message=_("Successfully deleted photo '%s'") % title)
    
    return HttpResponseRedirect(redirect_to)
