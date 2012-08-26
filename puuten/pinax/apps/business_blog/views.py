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
from blog.models import *
from share.models import Share
from wishing_list.models import Wish
from business_blog.models import *
from business_blog.forms import *
from business.models import *



if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False

def blogs(request, business_id, template_name="business_blog/blogs.html"):
    business = BusinessProfile.objects.get(pk=int(business_id))
    business_app_list = BusinessApp.objects.filter(local_business=business)
    blogs = BusinessBlog.objects.filter(status=2).select_related(depth=1).order_by("-publish")
    blogs = blogs.filter(owner_id = business_id)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    return render_to_response(template_name, {
        "blogs": blogs,
        "business": business,
        "business_app_list": business_app_list,
        "is_manager": is_manager,
    }, context_instance=RequestContext(request))
    
@login_required
def new(request, business_id, form_class=BusinessBlogForm, template_name="business_blog/new.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = form_class(request.user, request.POST)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                blog.body = blog.body.replace("\n","<br>")
                blog.body = blog.body.replace("\n\r","<br>")
                blog.body = blog.body.replace("\r","<br>")
                blog.owner_type = 2
                blog.owner_id = int(business_id)
                business = BusinessProfile.objects.get(pk=business_id)
                blog.latitude = business.latitude
                blog.longitude = business.longitude
                if getattr(settings, 'BEHIND_PROXY', False):
                    blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    blog.creator_ip = request.META['REMOTE_ADDR']
                blog.save()
                # @@@ should message be different if published?
                request.user.message_set.create(message=_("Successfully saved blog '%s'") % blog.title)
                return HttpResponseRedirect(reverse("business_blogs", args=business_id))
    blog_form = form_class()
    local_business = BusinessProfile.objects.get(pk=business_id)
    is_manager = Manageship.objects.are_conbined(request.user, local_business)
    business_app_list = BusinessApp.objects.filter(local_business=local_business)
    return render_to_response(template_name, {
        "business":local_business,
        "business_app_list":business_app_list,
        "blog_form": blog_form,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))

@login_required    
def edit(request, business_id, blog_id, form_class=BusinessBlogForm, template_name="business_blog/edit.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    blog_instance = BusinessBlog.objects.get(pk=blog_id)
    if request.method == "POST":
        if not is_manager:
            request.user.message_set.create(message="You can't edit posts that aren't yours")
            return HttpResponseRedirect(reverse("business_blogs", args=business_id))
        if request.POST["action"] == "update":
            blog_form = form_class(request.user, request.POST, instance=blog_instance)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.save()
                request.user.message_set.create(message=_("Successfully updated blog '%s'") % blog.title)                
                return HttpResponseRedirect(reverse("business_blogs", args=business_id))
        else:
            blog_form = form_class(instance=blog_instance)
    else:
        blog_form = form_class(instance=blog_instance)
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "business":business,
        "business_app_list":business_app_list,
        "blog":blog_instance,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))
    
@login_required
def blog(request, business_id, blog_id, wish_model = Wish, template_name="business_blog/blog.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    blog_instance = BusinessBlog.objects.get(pk=blog_id)
    if request.method == "POST":
        if request.POST["action"] == "add_to_my_wishing_list":
            if Wish.objects.filter(shared_type=ContentType.objects.get(model=blog_instance.get_type()), shared_id=blog_instance.id).count() > 0:
                request.user.message_set.create(message="You had ready added it to your wishing list.")
            else:
                new_wish = wish_model(owner=request.user, shared=blog_instance, tags="wishing_list")
                new_wish.save()
                return HttpResponseRedirect(reverse("your_wishing_list"))
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "post":blog_instance,
        "is_manager":is_manager,
    },context_instance=RequestContext(request))
    
def destroy(request, business_id, blog_id):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    blog_instance = BusinessBlog.objects.get(pk=blog_id)
    title = blog_instance.title
    if is_manager:
        if request.method == "POST" and request.POST["action"] == "delete":
            blog_instance.delete()
            request.user.message_set.create(message=_("Successfully deleted event '%s'") % title)
            return HttpResponseRedirect(reverse("business_blogs", args=business_id))
        else:
            return HttpResponseRedirect(reverse("business_blogs", args=business_id))
    else:
        request.user.message_set.create(message="You can't delete this event")
        return HttpResponseRedirect(reverse("business_blogs", args=business_id))