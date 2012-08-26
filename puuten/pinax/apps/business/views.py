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

from django.utils import simplejson as json
from django.utils.safestring import mark_safe

from business.models import *
from business.forms import *
from blog.models import Post
from blog.forms import *
from microblogging.models import Following
from event.models import *
from business_photos.forms import BusinessPhotoUploadForm
from business_sina.models import *
from business_sina_weibo.models import TempTagForInfo
import uuid

@login_required
def single_business(request, id, template_name="business/single_business.html"):
    business = BusinessProfile.objects.get(pk=int(id))
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
#   for instance in business_app_list:
#       print instance.app_name
#       print instance.url
    if not business:
        raise Http404
    if request.user.is_authenticated():
        is_following = Following.objects.is_following(request.user, business)
    else:
        is_following = False
#    managers = Manageship.objects.manager_for_business(business)
    return render_to_response(template_name, {
        "business": business,
        "business_app_list": business_app_list,
        "is_manager":is_manager,
#        "managers": managers, 
        "posts": Event.objects.filter(owner_type=2, owner_id=business.id, upcoming_or_not=1),
        "is_following": is_following,
    }, context_instance=RequestContext(request))

@login_required
def business_profile(request, id, template_name="business/business_profile.html"):
    business = BusinessProfile.objects.get(pk=int(id))
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    if not business:
        raise Http404
    return render_to_response(template_name, {
        "business": business,
        "business_app_list": business_app_list,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))



@login_required
def your_business(request, template_name="business/your_business.html"):
    edit_profile_url = "/profiles/edit/"
    if not request.user.get_profile().name:
        return HttpResponseRedirect(edit_profile_url)
    return render_to_response(template_name, {
        "business_approved": BusinessProfile.objects.filter(creator=request.user, status='1'),
        "business_pending": BusinessProfile.objects.filter(creator=request.user, status='2'),
    }, context_instance=RequestContext(request))

def your_collection(request, template_name="business/your_collection.html"):
    your_collection = Following.objects.business_you_follow(request.user)
    result = BSAdmin.objects.filter(b_s_admin=request.user)
    if result:
        bs_admin_or_not=True
    else:
        bs_admin_or_not=False
    if request.method == "POST":
        if not "action" in request.POST:
            if request.POST['lat']:
                business_sina = BSInfo.objects.get(pk=int(request.POST['business_id']))
                business_sina.new_name = request.POST['business_new_name']
                business_sina.address  = request.POST['business_address']
                business_sina.latitude = request.POST['lat']
                business_sina.longitude = request.POST['lng']
                business_sina.status = 1
                business_sina.save()
            else:
                business_sina = BSInfo.objects.get(pk=int(request.POST['business_id']))
                business_sina.new_name = request.POST['business_new_name']
                business_sina.address  = request.POST['business_address']
                business_sina.status = 3
                business_sina.save()
            data = business_sina.id
            data = json.dumps(data)
            return HttpResponse(mark_safe(data))
        if request.POST['action']=='reset':
            business_sina_list = BSInfo.objects.filter(status__gt=2)
            for instance in business_sina_list:
                instance.status = 2
                instance.save()
        if request.POST['action']=='recover':
            business_sina_list = BSInfo.objects.filter(status=1)
            for instance in business_sina_list:
                instance.status = 2
                instance.save()
    business_sina_list_active = BSInfo.objects.order_by('id').filter(status = 1)
    business_sina_list_negative = BSInfo.objects.order_by('location').filter(status__gt = 2)
    business_count = BSInfo.objects.all().count()
    business_active_count = business_sina_list_active.count()
    business_negative_count = business_sina_list_negative.count()

    return render_to_response(template_name, {
        "your_collection": your_collection,
        "bs_admin_or_not": bs_admin_or_not,
        "business_sina_list_active": business_sina_list_active,
        "business_sina_list_negative": business_sina_list_negative,
        "business_active_count":business_active_count,
        "business_negative_count":business_negative_count,
        "business_count":business_count,
    }, context_instance=RequestContext(request))

@login_required
def new(request, form_class=BusinessProfileForm, management_model=Manageship, template_name="business/new.html"):
    profile = request.user.get_profile()
    if request.method == "POST":
        if request.POST["action"] == "create":
            new_data = request.POST.copy()
            business_profile_form = form_class(request.POST)
            if business_profile_form.is_valid():
                business_profile = business_profile_form.save(commit=False)
                business_profile.creator = request.user
                business_profile.status = "2"
                business_profile.save()
                management = management_model(manager=request.user, local_business=business_profile)
                management.save()
                new_data['title'] = uuid.uuid1().__str__()
                new_data['safetylevel'] = '1'#Image.SAFETY_LEVEL 
                new_data["latitude"] = business_profile.latitude
                new_data["longitude"] = business_profile.longitude
                photo_form = BusinessPhotoUploadForm(request.user, new_data, request.FILES)
                if photo_form.is_valid():
                    photo = photo_form.save(commit=False)
                    photo.member = request.user
                    photo.is_public = True
                    photo.title = uuid.uuid1().__str__()
                    photo.safetylevel = '1'#Image.SAFETY_LEVEL 
                    photo.latitude = business_profile.latitude
                    photo.longitude = business_profile.longitude
                    photo.save()
                    surl = photo.get_display_url()
                    business_profile.picurl = surl
                    business_profile.save()
                request.user.message_set.create(message=_("Successfully create your business '%s'") % business_profile.name)
                return HttpResponseRedirect(reverse("your_business"))
        
    business_profile_form = form_class()

    return render_to_response(template_name, {
        "business_profile_form": business_profile_form,
        "profile": profile,
    }, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=BusinessProfileForm, **kwargs):
    template_name = kwargs.get("template_name", "business/edit.html")
    business = get_object_or_404(BusinessProfile, id=id)
    if request.method == "POST":
        if business.creator != request.user:
            request.user.message_set.create(message="You can't edit business profile that aren't yours")
            return HttpResponseRedirect(reverse("your_business"))

        if request.POST["action"] == "update":
            new_data = request.POST.copy()            
            business_profile_form = form_class(request.POST, instance=business)
            if business_profile_form.is_valid():
                business_profile = business_profile_form.save(commit=False)
                new_data['title'] = uuid.uuid1().__str__()
                new_data['safetylevel'] = '1'#Image.SAFETY_LEVEL 
                new_data["latitude"] = business_profile.latitude
                new_data["longitude"] = business_profile.longitude
                photo_form = BusinessPhotoUploadForm(request.user, new_data, request.FILES)
                if photo_form.is_valid():
                    photo = photo_form.save(commit=False)
                    photo.member = request.user
                    photo.is_public = True
                    photo.title = uuid.uuid1().__str__()
                    photo.safetylevel = '1'#Image.SAFETY_LEVEL 
                    photo.latitude = business_profile.latitude
                    photo.longitude = business_profile.longitude
                    photo.save()
                    surl = photo.get_display_url()
                if surl != None:
                    business_profile.picurl = surl
                business_profile.save()
                request.user.message_set.create(message=_("Successfully updated your business '%s'") % business.name)
                return HttpResponseRedirect(reverse("your_business"))
    else:
        business_profile_form = form_class(instance=business)

    return render_to_response(template_name, {
        "business_profile_form": business_profile_form,
        "business": business,
    }, context_instance=RequestContext(request))
    



@login_required
def destroy(request, id):
    business = BusinessProfile.objects.get(pk=id)
    if business.creator != request.user:
        request.user.message_set.create(message="You can't delete business that aren't yours")
        return HttpResponseRedirect(reverse("your_business"))

    if request.method == "POST" and request.POST["action"] == "delete":
        print business.id
        business.delete()
        return HttpResponseRedirect(reverse("your_business"))
    else:
        return HttpResponseRedirect(reverse("your_business"))

    return render_to_response(context_instance=RequestContext(request))

@login_required
def search(request, id, template_name="business/search.html", form_class=InviteManageForm, extra_context=None):
    if extra_context is None:
        extra_context = {}
    local_business = BusinessProfile.objects.get(pk=id)
    if request.user == local_business.creator:
        is_creator = True
    else:
        is_creator = False
    user = None
    search_terms = request.GET.get('search', '')
    if search_terms:
        #users = User.objects.filter(username__icontains=search_terms)
        users = User.objects.filter(username=search_terms)
        if not users:
            user = None
            invite_form = None
        else:
            user = users[0]
            is_manager = Manageship.objects.are_conbined(user, local_business)
            if is_manager:
                invite_form = None
                if request.method == "POST":
                    if request.POST.get("action") == "remove":
                        Manageship.objects.remove(user, local_business)
                        request.user.message_set.create(message=_("You have removed %(user)s from management") % {'user': user})
                        is_manager = False
                        invite_form = form_class(request.user, {
                            'local_business_id':id,
                            'to_user':user.username,
                            'to_user_id':user.id,
                            'message':ugettext(_("Please join us!")),
                        })
            else: 
                if request.POST.get("action") == "invite":
                    invite_form = InviteManageForm(request.user, request.POST)
                    if invite_form.is_valid():
                        invite_form.save()
                else:
                    invite_form = form_class(request.user, {
                        'local_business_id':id,
                        'to_user':user.username,
                        'to_user_id':user.id,
                        'message':ugettext("Please join us!"),
                    })
    else:
        invite_form = None
    return render_to_response(template_name, dict({
        'users': user,
        'search_terms': search_terms,
        'invite_form': invite_form,
        'is_creator': is_creator,
    }, **extra_context), context_instance=RequestContext(request))

def about(request, id, template_name="business/about.html"):
    business = BusinessProfile.objects.get(pk=id)
    managers = Manageship.objects.manager_for_business(business)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "managers": managers,
    }, context_instance=RequestContext(request))

def location(request, id, template_name="business/location.html"):
    business = BusinessProfile.objects.get(pk=id)
    return render_to_response(template_name, {
        "business":business,
    }, context_instance=RequestContext(request))
    
def blogs(request, id, template_name="business/blogs_business.html"):
    business = BusinessProfile.objects.get(pk=id)
    blogs = Post.objects.filter(owner_type=2, owner_id=id)
    return render_to_response(template_name, {
        "business": business,
        "blogs": blogs,
    }, context_instance=RequestContext(request))
def gallery(request, id, template_name="business/photos_business.html"):
    business = BusinessProfile.objects.get(pk=int(id))
    photos = Image.objects.filter(owner_type=2, owner_id=id)
    return render_to_response(template_name, {
        "photos": photos,
        "business": business,
    }, context_instance=RequestContext(request))
def menu(request, id, template_name="business/menu.html"):
    menus = Post.objects.filter(owner_type=2, owner_id=id, tags="menu")
    business = BusinessProfile.objects.get(pk=int(id))
    return render_to_response(template_name, {
        "menus": menus,
        "business": business,
    }, context_instance=RequestContext(request))

@login_required    
def apps(request, id, business_app=BusinessApp, template_name="business/business_apps.html"):
    if request.method == "POST":
        if request.POST["action"] == "submit":
 #           print request.POST
            app_list_int = []
            local_business = BusinessProfile.objects.get(pk=id)
            if request.POST['name']:
                business_app_list = BusinessApp.objects.filter(local_business=local_business)
                for app in business_app_list:
                    app.delete()
                app_list_str = request.POST['name'].split(",")
                for app_id in app_list_str:
                    if app_id:
                        app_list_int.append(int(app_id))
                for app_id in app_list_int:
                    app = App.objects.get(pk=app_id)
                    instance = business_app(local_business=local_business, app_id=app.id, url=app.url+str(id)+"/", app_name=app.name)
                    instance.save()
            business_app_list = BusinessApp.objects.filter(local_business=local_business)
            return HttpResponseRedirect(reverse("your_business"))
    app_list = App.objects.all()
    return render_to_response(template_name, {
        "app_list":app_list,
    }, context_instance=RequestContext(request))

@login_required    
def app_management(request, form_class=AppForm, app_class=App, template_name="business/business_app_management.html"):
    app_list = App.objects.all()
    bs_admins = BSAdmin.objects.all()
    tags = TempTagForInfo.objects.all()
    if request.method == "POST":
        if request.POST["action"] == "create":
            app = app_class(name=request.POST["name"], description=request.POST['description'], url=request.POST['url'])
            app.save()
            return HttpResponseRedirect(reverse("business_app_management"))
        elif request.POST["action"] == 'search':
            search_terms = request.POST.get('search', '')
            users = User.objects.filter(username__icontains=search_terms)
            app_form = form_class()
        elif request.POST["action"] == 'invite':
            invitation_id = request.POST.get("invitation_id", None)
            invited_user = User.objects.get(pk=invitation_id)
            bs_admin = BSAdmin(b_s_admin=invited_user, approved_or_not=True)
            bs_admin.save()
            return HttpResponseRedirect(reverse("business_app_management"))
        elif request.POST["action"]  == 'remove':
            remove_id = request.POST.get("remove_id", None)
            remove_user = User.objects.get(pk=remove_id)
            bs_admin = BSAdmin.objects.get(b_s_admin=remove_user)
            bs_admin.delete()
            return HttpResponseRedirect(reverse("business_app_management"))
        elif request.POST["action"] == 'add_tag':
            temp_tag = TempTagForInfo(tag=request.POST['tag'])
            temp_tag.save()
            return HttpResponseRedirect(reverse("business_app_management"))
        elif request.POST["action"] == 'delete_tag':
            tag_id = request.POST['tag_id']
            tag = TempTagForInfo.objects.get(pk=tag_id)
            tag.delete()
            return HttpResponseRedirect(reverse("business_app_management"))
        else:
            app_form = form_class()
            user = []
    else:
        app_form = form_class()
        users = []
    return render_to_response(template_name, { 
        "app_list":app_list,
        "app_form":app_form,
        "friends":users,
        "bs_admins":bs_admins,
        "tags":tags,
    }, context_instance=RequestContext(request))

@login_required    
def app_destroy(request, id):
    app_instance = App.objects.get(pk=id)
    business_app_list = BusinessApp.objects.filter(app_id=app_instance.id)
    if request.user.id != 1:
        request.user.message_set.create(message="You can't delete this app")
        return HttpResponseRedirect(reverse("business_app_management"))

    if request.method == "POST" and request.POST["action"] == "delete":
        app_instance.delete()
        for business_app_instance in business_app_list:
            business_app_instance.delete()
        return HttpResponseRedirect(reverse("business_app_management"))
    else:
        return HttpResponseRedirect(reverse("business_app_management"))

    return render_to_response(context_instance=RequestContext(request))

@login_required
def app_edit(request, id, form_class=AppForm, app_class=App, template_name="business/app_edit.html"):
    app = get_object_or_404(App, id=id)
    if request.method == "POST":
        if request.user.id != 1:
            request.user.message_set.create(message="You can't edit business_app data")
            return HttpResponseRedirect(reverse("your_business"))
        if request.POST["action"] == "update":
            app.name = request.POST["name"]
            app.description=request.POST['description']
            app.url=request.POST['url']
            app.save()
            business_app_list = BusinessApp.objects.filter(app_id=app.id)
            for business_app in business_app_list:
                business_app.app_name = app.name
                business_app.save()
            return HttpResponseRedirect(reverse("business_app_management"))
        else:
            app_form = form_class(instance=app)
    else:
        app_form = form_class(instance=app)
    return render_to_response(template_name, {
        "app_form":app_form,
        "app":app,
    }, context_instance=RequestContext(request))
