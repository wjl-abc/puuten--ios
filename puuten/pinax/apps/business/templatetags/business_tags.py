from django import template
from django.utils.translation import ugettext

from business.models import BusinessProfile
from business_sina.models import BSAdmin
#from contact.models import Contact
from event.models import Event
register = template.Library()

def business_window_info(business):
    name = business.name
    link = business.get_absolute_url()
    #contaction = Contact.objects.filter(business = business)
    events = Event.objects.filter(owner_type=2, owner_id=business.id, upcoming_or_not=1)
    info = "<div><div><h2><a href="+link+">"+name+"</a></h2></div><div><p class=number></p></div>"
    if events:
        for instance in events:
            info = info + "<div><h4><a href="+instance.get_absolute_url()+">"+instance.title+"<a></h4></div>"
    info = info+"</div>"
    return info
register.simple_tag(business_window_info)

def business_recommend_info(business):
    events = Event.objects.filter(owner_type=2, owner_id=business.id, upcoming_or_not=1)
    info = "<div>"
    if events: 
        for instance in events:
            info = info + "<div><h4><a href="+instance.get_absolute_url()+">"+instance.title+"<a></h4></div>"
    info = info+"</div>"
    return info
register.simple_tag(business_recommend_info)

def business_detail_info(business):
    name = business.name
    link = business.get_absolute_url()
    address = business.location
    #contaction = Contact.objects.filter(business = business)
    info = "<div><div><h2><a href="+link+">"+name+"</a></h2></div><div><p class=address>"+address+"</p></div></div>"
    return info
register.simple_tag(business_detail_info)
