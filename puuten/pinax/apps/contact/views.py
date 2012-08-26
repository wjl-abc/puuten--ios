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
from business.models import *
from contact.models import *
from contact.forms import *
def show(request, business_id, form_class=ContactForm, template_name="contact/show.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    contact_case = Contact.objects.filter(business = business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    if contact_case:
        contact_case = contact_case[0]
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "contact_case": contact_case,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))
    
def new(request, business_id, form_class=ContactForm, contact_model=Contact, template_name="contact/new.html"):
    business = BusinessProfile.objects.get(pk=business_id)
    business_app_list = BusinessApp.objects.filter(local_business=business)
    is_manager = Manageship.objects.are_conbined(request.user, business)
    contact_form = form_class()
    if request.method == "POST":
        if request.POST["action"] == "create":
            contact = contact_model(business=business, address=request.POST['address'], email=request.POST['email'], number=request.POST['number'], schedule=request.POST['schedule'], direction=request.POST['direction'])
            contact.save()
            return HttpResponseRedirect(reverse("business_contact", args=business_id))
    return render_to_response(template_name, {
        "business":business,
        "business_app_list":business_app_list,
        "contact_form": contact_form,
        "is_manager":is_manager,
    }, context_instance=RequestContext(request))