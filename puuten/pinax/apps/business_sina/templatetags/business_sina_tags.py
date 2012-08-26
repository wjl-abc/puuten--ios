# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta, datetime
from django import template
from django.utils.translation import ugettext
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson as json
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from business_sina.models import BSInfo, BSAdmin
from ijustdated.models import Dating
from wat.models import Buzz
from business_sina_weibo.models import WeiBo
import sys
import copy

reload(sys)
sys.setdefaultencoding('utf-8') 

register = template.Library()

def is_bs_admin_or_not(self):
    result = BSAdmin.objects.filter(b_s_admin=self)
    if result[0]:
        flag = True
    else:
        flag = False
    return flag
register.simple_tag(is_bs_admin_or_not)

@register.inclusion_tag("weibo/weibo_item.html")

def wb_in_window(bs_id, wb_id, flag):
    wb = WeiBo.objects.get(pk=wb_id)
    head = """<div id=%s class='blog-post clearfix'><div class='blog-post-tease'>"""%(wb_id)
    body = wb.sina_text
    
    if wb.retweeted_sina_id is not None:
        wb.retweeted_post = WeiBo.objects.get(sina_id=wb.retweeted_sina_id)
        wb.retweeted_post.sina_user = json.loads(wb.retweeted_post.sina_user)
        sina_user = copy.copy(wb.sina_user)
        temp_idstr = wb.retweeted_post.sina_user['idstr']
        temp_name = wb.retweeted_post.sina_user['name']
        wb.retweeted_post.sina_user = sina_user
    else:
        wb.retweeted_post = ""
    if wb.retweeted_post:
        subhead = """<div id=%s class='blog-post clearfix retweeted'><div >Retweeted from :<a href='http://www.weibo.com/%s' target='_blank'>@%s</a></div><div class='blog-post-tease'>"""%(wb.retweeted_post.sina_id, temp_idstr, temp_name)
        subbody = wb.retweeted_post.sina_text
        subfoot = """</div></div></div>"""
        body = """<div class="blog-post-retweeted">"""+body+subhead+subbody+subfoot
    foot = """</div></div>"""
    wb_info = head+body+foot
    if flag:
        attached_head = "<div>"
        attached_foot = "</div>"
        dating_link = """<a href=/ijustdated/new/?bs_id=%s&wb=%s>Invite him/her    </a>"""% (bs_id, wb_id)
        wat_link = """<a href=/wat/new/?bs_id=%s&wb=%s>Invite friends to attend    </a>"""% (bs_id, wb_id)
        if wb.num_of_wishing():
            check_wishing_list_user = """<a href=%s rel='facebox'>%s already added it to the wishing list</a>"""% (wb.get_wishing_list_user_url(), wb.num_of_wishing())
        else:
            check_wishing_list_user = ""
        wish_list_link = """<form method='POST' action=%s>
                        <div class='form_block'>
                            <input type='hidden' name='action' value='add_to_my_wishing_list' />
                            <input type='submit' value='add to my wishing list' />
                        </div>
                    </form>"""%( wb.add_2_wishing_list())
        wb_info = wb_info  +  attached_head+dating_link  +   wat_link  +  check_wishing_list_user  +   wish_list_link  +  attached_foot
    return wb_info
register.simple_tag(wb_in_window)

def new_window_info_bs(id):
    bs = BSInfo.objects.get(pk=id)
    head = """<div><a href=%s  title=%s><img usercard='' id=%s title=%s alt='' width='50' height='50' src=%s></a></div><div><p>%s<p></div>"""% (bs.get_absolute_url(), bs.name, bs.sina_id, bs.name, bs.avatar, bs.tags)
    num_dating = Dating.objects.filter(reference_bs=bs.id).count()
    num_buzz   = Dating.objects.filter(reference_bs=bs.id).count()
    #head = """<div><a href=%s>%s</a></div><div><p>%s<p></div>"""% (bs.get_absolute_url(), bs.name, bs.tags)
    #url  = """/ijustdated/new/?bs_id=%s"""(instance.id)
    if num_dating>0:
        dating="""<a href=/ijustdated/new/?bs_id=%s>Invite him/her(%s)</a><a>'   '</a>"""%(bs.id, num_dating)
    else:
        dating="""<a href=/ijustdated/new/?bs_id=%s>Invite him/her</a><a>'   '</a>"""%(bs.id)
    if num_buzz>0:
        buzz="""<a href=/wat/new/?bs_id=%s>Invite friends to attend(%s)</a>"""%(bs.id, num_buzz)
    else:
        buzz="""<a href=/wat/new/?bs_id=%s>Invite friends to attend</a>"""%(bs.id)
    wish_list = """<form method='POST' action=''>
                       <div class='form_block'>
                           <input type='hidden' name='action' value='add_to_my_wishing_list' />
                           <input type='hidden' name='bs_id' value='%s' />
                           <input type='submit' value='add to my wishing list' />
                       </div>
                   </form>"""%(bs.id)
    #  下一条中的 status＝4  只是临时试用， 之后还要添加时间属性
    wb_recommended = WeiBo.objects.filter(sina_userid=bs.sina_id, status = "2")
    wb_list = WeiBo.objects.order_by("created_at").filter(sina_userid=bs.sina_id).exclude(status="2")
    if wb_recommended.count()<5:
        num_wb_inneed = 5 - wb_recommended.count()
        for instance in wb_recommended:
            head = head + wb_in_window(id, instance.id, 1)
    else:
        num_wb_inneed = 0
    if num_wb_inneed>wb_list.count():
        num_wb_inneed = wb_list.count()
    if num_wb_inneed:
        for i in range(0, num_wb_inneed):
            head = head + wb_in_window(id, wb_list[i].id, 0)
    if wb_recommended.count()<1:
        head = head + "<div>"  +  dating  +  buzz  +  wish_list  +  "</div>"
    return head
register.simple_tag(new_window_info_bs)
       
def window_info_bs(id):
    instance = BSInfo.objects.get(pk=id)
    num_dating = Dating.objects.filter(reference_bs=instance.id).count()
    num_buzz   = Dating.objects.filter(reference_bs=instance.id).count()
    head = """<div><a href=%s>%s</a></div><div><p>%s<p></div>"""% (instance.get_absolute_url(), instance.name, instance.tags)
    #url  = """/ijustdated/new/?bs_id=%s"""(instance.id)
    if num_dating>0:
        dating="""<a href=/ijustdated/new/?bs_id=%s>Invite him/her(%s)</a>"""%(instance.id, num_dating)
    else:
        dating="""<a href=/ijustdated/new/?bs_id=%s>Invite him/her</a>"""%(instance.id)
    if num_buzz>0:
        buzz="""<a href=/wat/new/?bs_id=%s>Invite friends to attend(%s)</a>"""%(instance.id, num_buzz)
    else:
        buzz="""<a href=/wat/new/?bs_id=%s>Invite friends to attend</a>"""%(instance.id)
    wish_list = """<form method='POST' action=''><div class='form_block'><input type='hidden' name='action' value='add_to_my_wishing_list' /><input type='hidden' name='bs_id' value='%s' /><input type='submit' value='add to my wishing list' /></div></form>"""%(instance.id)
    foot = "<div>"+dating+buzz+wish_list+"</div>"
    return head+foot
register.simple_tag(window_info_bs)

def get_city(instance):
    DC = "北京天津上海重庆"
    location = instance.location
    location = location.split(' ')
    if len(location)==1:
        return location[0]
    elif DC.find(location[0])>=0:
        return location[0]
    else:
        return location[1]
register.simple_tag(get_city)

def get_city_id(id):
    business_sina = BSInfo.objects.get(pk=id)
    city = get_city(business_sina)
    return city
register.simple_tag(get_city_id)

def get_business_tag(bs):
    tags=bs.tags.split(" ")
    result = ""
    for tag in tags:
        if tag:
            temp = """<input type='checkbox' name='items_tag' checked value=%s /><a>%s</a>"""%(tag, tag)
            result = result + temp
    return result
register.simple_tag(get_business_tag)