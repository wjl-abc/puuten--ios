#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PuuterTagManager(models.Manager):
    pass


# Create your models here.
class PuuterTag(models.Model):
    """
    A tag.
    类型字段以后扩展使用，表示大目录还是以后统计的，或推荐的
    """
    
    Tag_Type_Choices = (
        (1, _('category')),
        (2, _('suggestion')),
        (3, _('frequency')),
    )
    
    name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)
    tag_type = models.IntegerField(_('tag_type'), choices=Tag_Type_Choices, default=1)
    
    objects = PuuterTagManager()
    
    class Meta:
        db_table = "tag_app_puutertag" 
        ordering = ('name',)
        verbose_name = _('puutertag')
        verbose_name_plural = _('puutertags')

    def __unicode__(self):
        return self.name
