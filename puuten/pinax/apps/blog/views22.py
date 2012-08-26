import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from blog.models import Post
from blog.forms import *
from share.models import Share
from share.forms import *
from info_glue.models import Glueship
from info_glue.forms import *
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

def blogs(request, id=None, template_name="blog/blogs.html"):
    blogs = Post.objects.filter(status=2).select_related(depth=1).order_by("-publish")
    if id is not None:
        user = get_object_or_404(User, id=id)
        blogs = blogs.filter(author=user)
    return render_to_response(template_name, {
        "blogs": blogs,
    }, context_instance=RequestContext(request))

def post(request, type_, year, month, id,
         template_name="blog/post.html", share_model = Share):
    post = Post.objects.filter(id=int(id), publish__year=int(year), publish__month=int(month))
    if not post:
        raise Http404

    if post[0].status == 1 and post[0].author != request.user:
        raise Http404
    friends = []
    for friendship in Glueship.objects.filter(a_id=post[0].id, a_type=ContentType.objects.get(model=post[0].get_type())):
        friends.append(friendship.branch_b)
    for friendship in Glueship.objects.filter(b_id=post[0].id, b_type=ContentType.objects.get(model=post[0].get_type())):
        friends.append(friendship.branch_a)
    for friend in friends:
        print friend.get_absolute_url()
    if request.method == "POST":
        if request.POST["action"] == "share":
            if Share.objects.filter(shared_type=ContentType.objects.get(model=post[0].get_type()), shared_id=post[0].id).count() > 0:
                request.user.message_set.create(message="You have already shared this blog")
                return HttpResponseRedirect(reverse("blog_list_yours"))
            else:
                new_share = share_model(owner=request.user, shared=post[0])
                new_share.save()
            
    return render_to_response(template_name, {
        "post": post[0],
        "friends": friends,
    }, context_instance=RequestContext(request))

@login_required
def your_posts(request, template_name="blog/your_posts.html"):
    edit_profile_url = "/profiles/edit/"
    if not request.user.get_profile().name:
        return HttpResponseRedirect(edit_profile_url)
    return render_to_response(template_name, {
        "profile":request.user.get_profile(),
        "blogs": Post.objects.filter(author=request.user),
    }, context_instance=RequestContext(request))

@login_required
def destroy(request, id):
    post = Post.objects.get(pk=id)
    user = request.user
    title = post.title
    if post.author != request.user:
            request.user.message_set.create(message="You can't delete posts that aren't yours")
            return HttpResponseRedirect(reverse("blog_list_yours"))

    if request.method == "POST" and request.POST["action"] == "delete":
        post.delete()
        request.user.message_set.create(message=_("Successfully deleted post '%s'") % title)
        return HttpResponseRedirect(reverse("blog_list_yours"))
    else:
        return HttpResponseRedirect(reverse("blog_list_yours"))

    return render_to_response(context_instance=RequestContext(request))

@login_required
def new(request, form_class=BlogForm, template_name="blog/new.html"):
    profile = request.user.get_profile()
    edit_profile_url = "/profiles/edit/"
    if not profile.name:
        return HttpResponseRedirect(edit_profile_url)
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = form_class(request.user, request.POST)
            if blog_form.is_valid():
                blog_form.save()
                # @@@ should message be different if published?
                request.user.message_set.create(message=_("Successfully saved post '%s'") % blog_form.title)
                if notification:
                    if blog_form.status == 2: # published
                        if friends: # @@@ might be worth having a shortcut for sending to all friends
                            notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog_form.author)), "blog_friend_post", {"post": blog})
                if request.POST["owner_id"]:
                    return HttpResponseRedirect(reverse("single_business", args=(int(request.POST["owner_id"]),)))
                else:
                    return HttpResponseRedirect(reverse("blog_list_yours"))
            if request.POST["owner_id"]:
                something = int(request.POST["owner_id"])
            else:
                something = None
        else:
            blog_form = form_class()
            something = request.GET.get("something", None)
            if something:
                blog_form.fields['owner_id'].initial = u"%s" % something
    else:
        blog_form = form_class()
        something = request.GET.get("something", None)
        is_manager = True
        if something:
            blog_form.fields['owner_id'].initial = u"%s" % something
            local_business = BusinessProfile.objects.get(pk=something)
            is_manager = Manageship.objects.are_conbined(request.user, local_business)
            print is_manager
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "profile": profile,
        "something":something,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))

@login_required
def glue(request, form_class=BlogForm, glue_model=Glueship, template_name="blog/glue.html"):
    profile = request.user.get_profile()
    reference_id = request.GET.get("a_id", None)
    reference_type = request.GET.get("a_type", None)
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = form_class(request.user, request.POST)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                blog.body = blog.body.replace("\n","<br>")
                blog.body = blog.body.replace("\n\r","<br>")
                blog.body = blog.body.replace("\r","<br>")
                if getattr(settings, 'BEHIND_PROXY', False):
                    blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    blog.creator_ip = request.META['REMOTE_ADDR']
                blog.save()
                p = glue_model(branch_b=blog, a_id=reference_id, a_type=ContentType.objects.get(model=reference_type), created_by=request.user)
                p.save()
                # @@@ should message be different if published?
                request.user.message_set.create(message=_("Successfully saved post '%s'") % blog.title)
                if notification:
                    if blog.status == 2: # published
                        if friends: # @@@ might be worth having a shortcut for sending to all friends
                            notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", {"post": blog})
                
                return HttpResponseRedirect(reverse("blog_list_yours"))
        else:
            blog_form = form_class()
    else:
        blog_form = form_class()
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "profile": profile,
    }, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=BlogForm, template_name="blog/edit.html"):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if post.author != request.user:
            request.user.message_set.create(message="You can't edit posts that aren't yours")
            return HttpResponseRedirect(reverse("blog_list_yours"))
        if request.POST["action"] == "update":
            blog_form = form_class(request.user, request.POST, instance=post)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.save()
                request.user.message_set.create(message=_("Successfully updated post '%s'") % blog.title)
                if notification:
                    if blog.status == 2: # published
                        if friends: # @@@ might be worth having a shortcut for sending to all friends
                            notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", {"post": blog})
                
                return HttpResponseRedirect(reverse("blog_list_yours"))
        else:
            blog_form = form_class(instance=post)
    else:
        blog_form = form_class(instance=post)
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "post": post,
    }, context_instance=RequestContext(request))
