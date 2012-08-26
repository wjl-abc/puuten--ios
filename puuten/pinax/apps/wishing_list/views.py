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
from django.conf import settings
from tagging.models import Tag, TaggedItem
from wishing_list.models import *
from share.models import Share
from blog.models import Post
from blog.forms import *
from business_sina.models import BSInfo
from business_sina_weibo.models import WeiBo

def your_wishing_list(request, template_name="wishing_list/your_wishing_list.html"):
    wishes = Wish.objects.filter(owner=request.user)
    return render_to_response(template_name, {
        'wishing_list': Wish.objects.filter(owner=request.user),
    }, context_instance=RequestContext(request))
    
def new(request, form_class=BlogForm, template_name="wishing_list/new.html"):
    profile = request.user.get_profile()
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = form_class(request.user, request.POST)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                blog.owner_type = 1
                if getattr(settings, 'BEHIND_PROXY', False):
                    blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    blog.creator_ip = request.META['REMOTE_ADDR']
                blog.save()
                new_wishing = Wish(owner=request.user, shared=blog, tags="wishing_list")
                new_wishing.save()
                return HttpResponseRedirect(reverse("your_wishing_list"))
        else:
            blog_form = form_class()
    else:
        blog_form = form_class()
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "profile": profile,
    }, context_instance=RequestContext(request))

@login_required
def destroy(request, id):
    wish = Wish.objects.get(pk=id)
    user = request.user
    
    if wish.owner != request.user:
            request.user.message_set.create(message="You can't delete this from the wishing list that aren't yours")
            return HttpResponseRedirect(reverse("your_wishing_list"))

    if request.method == "POST" and request.POST["action"] == "delete":
        wish.delete()
        return HttpResponseRedirect(reverse("your_wishing_list"))
    else:
        return HttpResponseRedirect(reverse("your_wishing_list"))

    return render_to_response(context_instance=RequestContext(request))

def dating_and_wishing(request, id, template_name="wishing_list/dating_and_wishing.html"):
    user = get_object_or_404(User, id=id)
    return render_to_response(template_name, {
        'wishing_list': Wish.objects.filter(owner=user),
        'user':user,
    }, context_instance=RequestContext(request))
    
def user_list(request, type_id, shared_id, template_name="wishing_list/user_list.html"):
    wishing_list = Wish.objects.filter(content_type = type_id, shared_id=shared_id)
    wb = ""
    if int(type_id)==3:
        wb = WeiBo.objects.get(pk=shared_id)
    user_list = []
    for instance in wishing_list:
        user_list.append(instance.owner)
    return render_to_response(template_name, {
        'user_list': user_list,
        'wb':wb,
    }, context_instance=RequestContext(request))
    
