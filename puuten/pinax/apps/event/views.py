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
from event.models import *
from event.forms import *
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

def events(request, business_id, template_name="event/events.html"):
    business = BusinessProfile.objects.get(pk=int(business_id))
    business_app_list = BusinessApp.objects.filter(local_business=business)
    events = Event.objects.filter(status=2).select_related(depth=1).order_by("-publish")
    events = events.filter(owner_id = business_id)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    return render_to_response(template_name, {
        "events": events,
        "business": business,
        "business_app_list": business_app_list,
        "is_manager": is_manager,
    }, context_instance=RequestContext(request))
    
@login_required
def new(request, business_id, form_class=EventForm, template_name="event/new.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            event_form = form_class(request.user, request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.author = request.user
                event.body = event.body.replace("\n","<br>")
                event.body = event.body.replace("\n\r","<br>")
                event.body = event.body.replace("\r","<br>")
                event.owner_type = 2
                event.owner_id = int(business_id)
                business = BusinessProfile.objects.get(pk=business_id)
                event.latitude = business.latitude
                event.longitude = business.longitude
                if getattr(settings, 'BEHIND_PROXY', False):
                    event.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    event.creator_ip = request.META['REMOTE_ADDR']
                event.save()
                # @@@ should message be different if published?
                request.user.message_set.create(message=_("Successfully saved event '%s'") % event.title)
                return HttpResponseRedirect(reverse("business_events", args=business_id))
    event_form = form_class()
    local_business = BusinessProfile.objects.get(pk=business_id)
    is_manager = Manageship.objects.are_conbined(request.user, local_business)
    business_app_list = BusinessApp.objects.filter(local_business=local_business)
    return render_to_response(template_name, {
        "business":local_business,
        "business_app_list":business_app_list,
        "event_form": event_form,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))
    
@login_required
def event(request, business_id, event_id, wish_model=Wish, template_name="event/event.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    event_instance = Event.objects.get(pk=event_id)
    if request.method == "POST":
        if request.POST["action"] == "add_to_my_wishing_list":
            if Wish.objects.filter(shared_type=ContentType.objects.get(model=event_instance.get_type()), shared_id=event_instance.id).count() > 0:
                request.user.message_set.create(message="You had ready added it to your wishing list.")
            else:
                new_wish = wish_model(owner=request.user, shared=event_instance, tags="wishing_list")
                new_wish.save()
                return HttpResponseRedirect(reverse("your_wishing_list"))
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "event":event_instance,
        "is_manager":is_manager,
    },context_instance=RequestContext(request))

@login_required    
def edit(request, business_id, event_id, form_class=EventForm, template_name="event/edit.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    event_instance = Event.objects.get(pk=event_id)
    if request.method == "POST":
        if not is_manager:
            request.user.message_set.create(message="You can't edit events that aren't yours")
            return HttpResponseRedirect(reverse("business_events", args=business_id))
        if request.POST["action"] == "update":
            event_form = form_class(request.user, request.POST, instance=event_instance)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.save()
                request.user.message_set.create(message=_("Successfully updated event '%s'") % event.title)                
                return HttpResponseRedirect(reverse("business_events", args=business_id))
        else:
            event_form = form_class(instance=event_instance)
    else:
        event_form = form_class(instance=event_instance)
    return render_to_response(template_name, {
        "event_form": event_form,
        "business":business,
        "business_app_list":business_app_list,
        "event":event_instance,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))
    
def destroy(request, business_id, event_id):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    event_instance = Event.objects.get(pk=event_id)
    title = event_instance.title
    if is_manager:
        if request.method == "POST" and request.POST["action"] == "delete":
            event_instance.delete()
            request.user.message_set.create(message=_("Successfully deleted event '%s'") % title)
            return HttpResponseRedirect(reverse("business_events", args=business_id))
        else:
            return HttpResponseRedirect(reverse("business_events", args=business_id))
    else:
        request.user.message_set.create(message="You can't delete this event")
        return HttpResponseRedirect(reverse("business_events", args=business_id))

def switch(request, business_id, event_id):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    event_instance = Event.objects.get(pk=event_id)
    if is_manager:
            event_instance.upcoming_or_not=2
            event_instance.save()
            return HttpResponseRedirect(reverse("single_business", args=business_id))
    else:
        return HttpResponseRedirect(reverse("single_business", args=business_id))