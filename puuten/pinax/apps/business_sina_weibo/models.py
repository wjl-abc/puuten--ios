from datetime import datetime, timedelta, date
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from business_sina.models import BigIntegerField, BSInfo
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag
from wishing_list.models import Wish



WEIBO_STATUS = (
    ("-1", "Not_Saved"),
    ("99", "Retweeted_Weibo"),
    ("1", "Not_Checked"),
    ("2", "Recommendation"),
    ("3", "Checked"),
    ("4", "Event_Suspected"),
    ("5", "Business_Suspected"),
    ("6", "Personal_Suspected")
    )
class WeiBo(models.Model):
    sina_id     = BigIntegerField(_('sina_id'), null=True, blank=True)
    sina_text   = models.CharField(_('sina_text'), max_length=500, null=True, blank=True)
    source      = models.CharField(_('source'), max_length=200, null=True, blank=True)
    original_pic= models.CharField(_('original_pic'), max_length=200, null=True, blank=True)
    thumbnail_pic= models.CharField(_('thumbnail_pic'), max_length=200, null=True, blank=True)
    bmiddle_pic= models.CharField(_('bmiddle_pic'), max_length=200, null=True, blank=True)
    sina_geo    = models.CharField(_('sina_geo'), max_length=200, null=True, blank=True)
    sina_userid = BigIntegerField(_('sina_userid'), null=True, blank=True)
    sina_user   = models.TextField(_('sina_user'), null=True, blank=True)
    retweeted_sina_id  = BigIntegerField(_('retweeted_sina_id'), null=True, blank=True)
    created_at  = models.DateTimeField(_('created at'), default=datetime.now)
    annotations = models.TextField(_('annotations'), null=True, blank=True)
    status = models.CharField(max_length=3, choices=WEIBO_STATUS, null=True, blank=True, default='1')
    tags        = TagField(_('tags'))
    reposts_count  = BigIntegerField(_('reposts_count'), null=True, blank=True)
    comments_count = BigIntegerField(_('comments_count'), null=True, blank=True)
    aspect_ratio = models.FloatField(_('aspect_ratio'), null=True, blank=True)
    
    
    def get_true_id(self):
        owner = BSInfo.objects.filter(sina_id=self.sina_userid)
        if owner.count()>0:
            return self.id
        else:
            wb = WeiBo.objects.filter(retweeted_sina_id=self.sina_id)
            if wb.count()>0:
                return wb[0].id
            else:
                return "bad"
    
    def get_owner_id(self):
        owner = BSInfo.objects.filter(sina_id=self.sina_userid)
        return owner[0].id
    
    def get_owner_name(self):
        owner = BSInfo.objects.filter(sina_id=self.sina_userid)
        return owner[0].name

    
    def get_owner_url(self):
        owner = BSInfo.objects.filter(sina_id=self.sina_userid)
        if owner.count()>0:
            owner=owner[0]
            return owner.get_absolute_url()
        else:
            wb = WeiBo.objects.filter(retweeted_sina_id=self.sina_id)[0]
            owner = BSInfo.objects.get(sina_id=wb.sina_userid)
            return owner.get_absolute_url()
    
    def get_pic_url(self):
        if self.original_pic:
            return self.original_pic
        elif self.retweeted_sina_id:
            wb=WeiBo.objects.get(sina_id=self.retweeted_sina_id)
            if wb.original_pic:
                return wb.original_pic
            else:
                bs=BSInfo.objects.get(sina_id=self.sina_userid)
                return bs.avatar
        else:
            bs=BSInfo.objects.get(sina_id=self.sina_userid)
            return bs.avatar
    def get_pic_url_mobile(self):
        if self.original_pic:
            return self.thumbnail_pic
        elif self.retweeted_sina_id:
            wb=WeiBo.objects.get(sina_id=self.retweeted_sina_id)
            if wb.original_pic:
                return wb.thumbnail_pic
            else:
                bs=BSInfo.objects.get(sina_id=self.sina_userid)
                return bs.avatar
        else:
            bs=BSInfo.objects.get(sina_id=self.sina_userid)
            return bs.avatar
    def get_aspect_ratio(self):
        if self.aspect_ratio:
            return self.aspect_ratio
        elif self.retweeted_sina_id:
            wb=WeiBo.objects.get(sina_id=self.retweeted_sina_id)
            if wb.aspect_ratio:
                return wb.aspect_ratio
            else:
                return 1
        else:
            return 1
    
    def add_2_wishing_list(self):
        return ('wb_2_wishing_list', None, {
                'wb_id': self.id
    })
    add_2_wishing_list = models.permalink(add_2_wishing_list)
    
    def get_wishing_list_user_url(self):
        return ('wishing_list_user_list', None, {
                'type_id':3,
                'shared_id':self.id,
    })
    get_wishing_list_user_url = models.permalink(get_wishing_list_user_url)    
    
    def get_type(self):
        return type(self).__name__.lower()
    
    def num_of_wishing(self):
        return Wish.objects.filter(content_type=3, shared_id=self.id).count()
    
    
class WeiBo_ImportConfig(models.Model):
    sina_uid        = BigIntegerField(_('sina_uid'), null=True, blank=True)
    sina_weiboid    = BigIntegerField(_('sina_weiboid'), null=True, blank=True)
    
class InfoDisplay(models.Model):
    info_owner_type  = models.ForeignKey(ContentType, related_name="info_owner_type")
    info_owner_id    = models.PositiveIntegerField()
    info_owner       = generic.GenericForeignKey('info_owner_type','info_owner_id')
    latitude         = models.FloatField(_('latitude'))
    longitude        = models.FloatField(_('longitude'))
    info_type        = models.ForeignKey(ContentType, related_name="info_type")
    info_id          = models.PositiveIntegerField()
    info             = generic.GenericForeignKey('info_type','info_id')
    tags             = TagField()
    created_at       = models.DateTimeField(_('created_at'), default=datetime.now)
    begin            = models.DateTimeField(_('begin'))
    end              = models.DateTimeField(_('end'))
    created_by       = models.ForeignKey(User, related_name="created_by")

class TempTagForInfo(models.Model):
    tag    =  models.TextField(_('new_tag'))
