from datetime import datetime

from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models import signals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# favour django-mailer but fall back to django.core.mail

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

class GlueshipManager(models.Manager):

    def friends_for_entity(self, entity):
        friends = []
        entity_type = type(entity).__name__.lower()
        if entity_type == 'tweetinstance':
            entity_type = 'tweet'
        for glueship in self.filter(a_id=entity.id, a_type=ContentType.objects.get(model=entity_type)).select_related(depth=1):
            friends.append({"friend": friendship.branch_b, "friendship": friendship})
        for glueship in self.filter(b_id=entity.id, b_type=ContentType.objects.get(model=entity_type)).select_related(depth=1):
            friends.append({"friend": friendship.branch_a, "friendship": friendship})
        return friends
    
    def are_glued(self, entity1, entity2):
        entity_type1 = type(entity1).__name__.lower()
        entity_type2 = type(entity2).__name__.lower()
        if entity_type1 == 'tweetinstance':
            entity_type1 = 'tweet'
        if entity_type2 == 'tweetinstance':
            entity_type2 = 'tweet' 
        if self.filter(a_id=entity1.id, a_type=ContentType.objects.get(model=entity_type1), b_id=entity2.id, b_type=ContentType.objects.get(model=entity_type2)).count() > 0:
            return True
        if self.filter(a_id=entity2.id, a_type=ContentType.objects.get(model=entity_type2), b_id=entity1.id, b_type=ContentType.objects.get(model=entity_type1)).count() > 0:
            return True
        return False

    def remove(self, entity1, entity2):
        entity_type1 = type(entity1).__name__.lower()
        entity_type2 = type(entity2).__name__.lower()
        if entity_type1 == 'tweetinstance':
            entity_type1 = 'tweet'
        if entity_type2 == 'tweetinstance':
            entity_type2 = 'tweet' 
        if self.filter(a_id=entity1.id, a_type=ContentType.objects.get(model=entity_type1), b_id=entity2.id, b_type=ContentType.objects.get(model=entity_type2)):
            glueship = self.filter(a_id=entity1.id, a_type=ContentType.objects.get(model=entity_type1), b_id=entity2.id, b_type=ContentType.objects.get(model=entity_type2))
        elif self.filter(a_id=entity2.id, a_type=ContentType.objects.get(model=entity_type2), b_id=entity1.id, b_type=ContentType.objects.get(model=entity_type1)):
            glueship = self.filter(a_id=entity2.id, a_type=ContentType.objects.get(model=entity_type2), b_id=entity1.id, b_type=ContentType.objects.get(model=entity_type1))
        glueship.delete()


class Glueship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """
    ENTITY_TYPE = (
        ("1", "BLOG"),
        ("2", "PHOTO"),
        ("3", "TWETTER"),
        ("4", "ALBUM"),
        ("5", "PERSONAL PAGE"),
        ("6", "BUSINESS PAGE"),
        ("7", "GROUP PAGE"),
    )

    TAG_TYPE = (
        ("1", "A"),
        ("2", "B"),
        ("3", "C"),
    )
    a_type      = models.ForeignKey(ContentType, related_name="a_type")
    a_id        = models.PositiveIntegerField()
    branch_a    = generic.GenericForeignKey('a_type','a_id')
    b_type      = models.ForeignKey(ContentType, related_name="b_type")
    b_id        = models.PositiveIntegerField()
    branch_b    = models.IntegerField('b_type','b_id')
    # @@@ relationship types
    tag         = models.CharField(max_length=1, choices=TAG_TYPE)
    created_at  = models.DateTimeField(auto_now=True, blank=True)
    created_by  = models.ForeignKey(User)
    
    class Meta:
        unique_together = (('a_type', 'a_id', 'b_type', 'b_id'),)
    def get_type_a(self):
        return type(self.branch_a).__name__.lower()
    def get_type_b(self):
        return type(self.branch_b).__name__.lower()
