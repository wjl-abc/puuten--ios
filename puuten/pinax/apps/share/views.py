from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings
from share.models import Share
from share.forms import *
from blog.models import Post
from business.models import BusinessProfile
import datetime

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False

@login_required
def your_share(request, template_name="share/your_share.html"):
    shares = Share.objects.filter(owner=request.user)
    shared_instances = []
    return render_to_response(template_name, {
        "shares":shares,
    }, context_instance = RequestContext(request))
    
@login_required
def destroy(request, id):
    share = Share.objects.get(pk=id)
    user = request.user
    
    if share.owner != request.user:
            request.user.message_set.create(message="You can't delete posts that aren't yours")
            return HttpResponseRedirect(reverse("your_share"))

    if request.method == "POST" and request.POST["action"] == "delete":
        share.delete()
        return HttpResponseRedirect(reverse("your_share"))
    else:
        return HttpResponseRedirect(reverse("your_share"))

    return render_to_response(context_instance=RequestContext(request))
