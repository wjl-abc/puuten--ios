from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
BUSINESS_CREATION_STATUS = (
    ("1", "Approved"),
    ("2", "Sent"),
    ("3", "Reject"),
    ("4", "Deleted"))
class BusinessAppllicationApprovement(models.Manager):
    def business_approvement(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="2")
class BusinessProfile(models.Model):
    creator      = models.ForeignKey(User)
    created_at   = models.DateTimeField(_('created at'), default=datetime.now)
    name         = models.CharField(_('name'), max_length=200)
    tags_extra            = TagField(_('tags'))
    about        = models.TextField(_('about'))
    website      = models.URLField(_('website'), blank=True, null=True)
    latitude     = models.FloatField(_('latitude'), default=39.904214)
    longitude    = models.FloatField(_('longitude'), default=116.407413)
    status = models.CharField(max_length=1, choices=BUSINESS_CREATION_STATUS)
    location     = models.CharField(_('location'), max_length=200)
    direction    = models.TextField(_('direction'), blank=True)
    picurl         = models.CharField(_('picurl'), max_length=200, null=True)
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ('single_business', None, {'id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_type(self):
        return type(self).__name__.lower()

class ManageshipManager(models.Manager):

    def manager_for_business(self, business):
        managers = []
        for manageship in self.filter(local_business=business).select_related(depth=1):
            managers.append({"manager": manageship.manager, "manageship": manageship})
        return managers
    
    def are_conbined(self, user, business):
        if self.filter(manager=user, local_business=business).count() > 0:
            return True
        return False

    def remove(self, user, business):
        if self.filter(manager=user, local_business=business):
            manageship = self.filter(manager=user, local_business=business)
        manageship.delete()

class Manageship(models.Model):
    """
    A manageship is an assocision between a manager(user) and a business
    """
    
    manager = models.ForeignKey(User)
    local_business = models.ForeignKey(BusinessProfile)
    # @@@ relationship types
    added = models.DateTimeField(default=datetime.now)
    
    objects = ManageshipManager()
    
    class Meta:
        unique_together = (('manager', 'local_business'),)

def manager_set_for(business):
    return set([obj["manager"] for obj in Manageship.objects.manager_for_business(business)])

INVITE_STATUS = (
    ("1", "Created"),
    ("2", "Sent"),
    ("3", "Failed"),
    ("4", "Expired"),
    ("5", "Accepted"),
    ("6", "Declined"),
    ("7", "Joined Independently"),
    ("8", "Deleted")
)

class ManageshipInvitationManager(models.Manager):
    def manage_invitations(self, *args, **kwargs):
        return self.filter(*args, **kwargs).exclude(status__in=["6", "8"])

class ManageshipInvitation(models.Model):
    """
    A manageship invite is an invitation from one user to another to be
    associated as management.
    """
    
    #from_user = models.ForeignKey(User, related_name="invitations_from")
    local_business = models.ForeignKey(BusinessProfile, related_name="local_business")
    from_user = models.ForeignKey(User, related_name="manage_invitations_from")
    to_user = models.ForeignKey(User, related_name="manage_invitations_to")
    message = models.TextField()
    sent = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=1, choices=INVITE_STATUS)
    
    objects = ManageshipInvitationManager()

    def accept(self):
        if not Manageship.objects.are_conbined(self.to_user, self.local_business):
            manageship = Manageship(manager=self.to_user, local_business=self.local_business)
            manageship.save()
            self.status = "5"
            self.save()
#            if notification:
#                notification.send([self.local_business.creator], "management_accept", {"invitation":self})
#                notification.send([self.to_user], "management_accept_sent", {"invitation":self})
            

    def decline(self):
        if not Manageship.objects.are_conbined(self.to_user, self.local_business):
            self.status = "6"
            self.save()

class App(models.Model):
    name        = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    url         = models.CharField(_('url'), max_length=200)
    
class BusinessApp(models.Model):
    local_business = models.ForeignKey(BusinessProfile, related_name="business")
    app_id         = models.PositiveIntegerField()
    app_name       = models.CharField(_('name'), max_length=200)
    url            = models.CharField(_('url'), max_length=200)
