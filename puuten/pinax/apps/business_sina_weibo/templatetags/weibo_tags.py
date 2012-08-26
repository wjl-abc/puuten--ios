# -*- coding: utf-8 -*-
import re
import sys
from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from avatar.templatetags.avatar_tags import avatar, avatar_url, avatar_user
from threadedcomments.templatetags.threadedcommentstags import get_comments_count
from django.utils import simplejson as json
from business_sina_weibo.models import WeiBo, TempTagForInfo
from business_sina.models import BSInfo
import copy
register = template.Library()

def weibo_pic_url(weibo):
    url=""
    if weibo.retweeted_sina_id is not None:
        wb = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)
        if wb.original_pic:
            url = wb.original_pic
        else:
            bs = BSInfo(sina_id=weibo.sina_userid)
            url = bs.avatar
    elif weibo.original_pic:
        url = weibo.original_pic
    else:
        bs = BSInfo(sina_id=weibo.sina_userid)
        url = bs.avatar
    return url
register.simple_tag(weibo_pic_url)

def weibo_pic_url_id(wb_id):
    url=""
    weibo = WeiBo.objects.get(pk=wb_id)
    if weibo.retweeted_sina_id is not None:
        weibo.retweeted_post = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)
        if weibo.retweeted_post.original_pic:
            url = weibo.retweeted_post.original_pic
        else:
            bs = BSInfo(sina_id=weibo.sina_userid)
            url = bs.avatar
    elif weibo.original_pic:
        url = weibo.original_pic
    else:
        bs = BSInfo(sina_id=weibo.sina_userid)
        url = bs.avatar
    return url
register.simple_tag(weibo_pic_url_id)

@register.inclusion_tag("weibo/weibo_item.html")
def show_weibo(weibo):
    #if weibo_post.retweeted_sina_id is not None and 
    #weibo_post.sina_user = json.read(weibo_post.sina_user)
    try:
        weibo.sina_text = weibo_text_filter(weibo.sina_text)
        if weibo.retweeted_sina_id is not None:
            weibo.retweeted_post = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)        
            weibo.retweeted_post.sina_user = json.loads(weibo.retweeted_post.sina_user)
            sina_user = copy.copy(weibo.sina_user)
            sina_user.idstr = weibo.retweeted_post.sina_user["idstr"]
            sina_user.name = weibo.retweeted_post.sina_user["name"]
            weibo.retweeted_post.sina_user = sina_user
            weibo.retweeted_post.sina_text = weibo_text_filter(weibo.retweeted_post.sina_text)
        else:
            weibo.retweeted_post = ""
    except:
        print "Unexpected error:", sys.exc_info()  
        weibo.retweeted_post = ""
    return {"weibo": weibo,
            "bs": BSInfo.objects.get(sina_id = weibo.sina_userid),
            "retweeted_weibo": weibo.retweeted_post
            }
    
@register.inclusion_tag("weibo/weibo_item_big.html")
def show_weibo_big(weibo):
    #if weibo_post.retweeted_sina_id is not None and 
    #weibo_post.sina_user = json.read(weibo_post.sina_user)
    try:
        weibo.sina_text = weibo_text_filter(weibo.sina_text)
        if weibo.retweeted_sina_id is not None:
            weibo.retweeted_post = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)        
            weibo.retweeted_post.sina_user = json.loads(weibo.retweeted_post.sina_user)
            sina_user = copy.copy(weibo.sina_user)
            sina_user.idstr = weibo.retweeted_post.sina_user["idstr"]
            sina_user.name = weibo.retweeted_post.sina_user["name"]
            weibo.retweeted_post.sina_user = sina_user
            weibo.retweeted_post.sina_text = weibo_text_filter(weibo.retweeted_post.sina_text)
        else:
            weibo.retweeted_post = ""
    except:
        print "Unexpected error:", sys.exc_info()  
        weibo.retweeted_post = ""
    return {"weibo": weibo,
            "bs": BSInfo.objects.get(sina_id = weibo.sina_userid),
            "retweeted_weibo": weibo.retweeted_post
            }

@register.inclusion_tag("weibo/only_weibo.html")
def only_weibo(weibo):
    try:
        weibo.sina_text = weibo_text_filter(weibo.sina_text)
        if weibo.retweeted_sina_id is not None:
            weibo.retweeted_post = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)        
            weibo.retweeted_post.sina_user = json.loads(weibo.retweeted_post.sina_user)
            sina_user = copy.copy(weibo.sina_user)
            sina_user.idstr = weibo.retweeted_post.sina_user["idstr"]
            sina_user.name = weibo.retweeted_post.sina_user["name"]
            weibo.retweeted_post.sina_user = sina_user
            weibo.retweeted_post.sina_text = weibo_text_filter(weibo.retweeted_post.sina_text)
        else:
            weibo.retweeted_post = ""
    except:
        print "Unexpected error:", sys.exc_info()  
        weibo.retweeted_post = ""
    return {"weibo": weibo,
            "bs": BSInfo.objects.get(sina_id = weibo.sina_userid),
            "retweeted_weibo": weibo.retweeted_post
            }

def weibo_text_filter(text):
    text = user_ref_re.sub(make_user_link, text)
    text = shorturl_show(text)
    text = facetext_to_facepic(text)
    return text

            
@register.inclusion_tag("weibo/weibo_item_attached.html")
def attach_weibo(weibo):
    #if weibo_post.retweeted_sina_id is not None and 
    #weibo_post.sina_user = json.read(weibo_post.sina_user)
    try:
        if weibo.retweeted_sina_id is not None:
            weibo.retweeted_post = WeiBo.objects.get(sina_id=weibo.retweeted_sina_id)        
            weibo.retweeted_post.sina_user = json.loads(weibo.retweeted_post.sina_user)
            sina_user = copy.copy(weibo.sina_user)
            sina_user.idstr = weibo.retweeted_post.sina_user["idstr"]
            sina_user.name = weibo.retweeted_post.sina_user["name"]
            weibo.retweeted_post.sina_user = sina_user
        else:
            weibo.retweeted_post = ""
    except:
        print "Unexpected error:", sys.exc_info()  
        weibo.retweeted_post = ""
    return {"weibo": weibo,
            "retweeted_weibo": weibo.retweeted_post
            }    
    
def show_temp_tags():
    tags = TempTagForInfo.objects.all()
    result = ""
    for instance in tags:
        temp = """<input class="form_input tags" type='checkbox' name='items' value=%s />%s"""%(instance.tag, instance.tag)
        result = result+temp
    return result

register.simple_tag(show_temp_tags)

def get_temp_tags():
    tags = TempTagForInfo.objects.all()
    result = ""
    for instance in tags:
        temp = """<a href="/home/event_lib/?t=%s">%s</a>"""%( instance.tag, instance.tag)
        result = result+" " + temp
    return result
register.simple_tag(get_temp_tags)

user_ref_re = re.compile(u'@([a-zA-Z0-9_\-\u4e00-\u9fa5])+')


def make_user_link(text):
    username = text.group()
    return """<a target="blank" href="%s">%s</a>""" % ("http://weibo.com/n/"+username[1:], username)

def shorturl_show(text):
    try:
        shorturl = re.search("http://t.cn/(.+)", text).group()
        if len(shorturl)>19:
            shorturl = shorturl[0:19]
        return text.replace(shorturl,'<a target="_blank" href='+shorturl+'>'+shorturl+'</a>')
    
    except:
        return text
def facetext_to_facepic(text):
    try:
        face_list = {'[伦敦奥火]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5a/lundunaohuo_thumb.gif" alt="伦敦奥火" title="伦敦奥火">',
        '[cai开心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e2/caikaixin_thumb.gif" alt="cai开心" title="cai开心">',
        '[cai晃头]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/22/caihuangtou_thumb.gif" alt="cai晃头" title="cai晃头">',
        '[不好意思]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b4/lxhbuhaoyisi_thumb.gif" alt="不好意思" title="不好意思">',
        '[加油啊]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/03/lxhjiayou_thumb.gif" alt="加油啊" title="加油啊">',
        '[亲一口]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/88/lxhqinyikou_thumb.gif" alt="亲一口" title="亲一口">',
        '[笑哈哈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/32/lxhwahaha_thumb.gif" alt="笑哈哈" title="笑哈哈">',
        '[din推撞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/dd/dintuizhuang_thumb.gif" alt="din推撞" title="din推撞">',
        '[lb味]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d1/lbwei_thumb.gif" alt="lb味" title="lb味">',
        '[bobo纠结]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f0/bobojiujie_thumb.gif" alt="bobo纠结" title="bobo纠结">',
        '[g头晕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/cf/guibao30touyun_thumb.gif" alt="g头晕" title="g头晕">',
        '[bed凌乱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/fa/brdlingluan_thumb.gif" alt="bed凌乱" title="bed凌乱">',
        '[织]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/41/zz2_thumb.gif" alt="织" title="织">',
        '[神马]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/60/horse2_thumb.gif" alt="神马" title="神马">',
        '[浮云]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/fuyun_thumb.gif" alt="浮云" title="浮云">',
        '[给力]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c9/geili_thumb.gif" alt="给力" title="给力">',
        '[围观]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f2/wg_thumb.gif" alt="围观" title="围观">',
        '[威武]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/vw_thumb.gif" alt="威武" title="威武">',
        '[熊猫]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/panda_thumb.gif" alt="熊猫" title="熊猫">',
        '[兔子]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/81/rabbit_thumb.gif" alt="兔子" title="兔子">',
        '[奥特曼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/otm_thumb.gif" alt="奥特曼" title="奥特曼">',
        '[囧]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/15/j_thumb.gif" alt="囧" title="囧">',
        '[互粉]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/hufen_thumb.gif" alt="互粉" title="互粉">',
        '[礼物]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c4/liwu_thumb.gif" alt="礼物" title="礼物">',
        '[呵呵]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ac/smilea_thumb.gif" alt="呵呵" title="呵呵">',
        '[嘻嘻]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0b/tootha_thumb.gif" alt="嘻嘻" title="嘻嘻">',
        '[哈哈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/laugh.gif" alt="哈哈" title="哈哈">',
        '[可爱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/14/tza_thumb.gif" alt="可爱" title="可爱">',
        '[可怜]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/kl_thumb.gif" alt="可怜" title="可怜">',
        '[挖鼻屎]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a0/kbsa_thumb.gif" alt="挖鼻屎" title="挖鼻屎">',
        '[吃惊]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f4/cj_thumb.gif" alt="吃惊" title="吃惊">',
        '[害羞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/shamea_thumb.gif" alt="害羞" title="害羞">',
        '[挤眼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c3/zy_thumb.gif" alt="挤眼" title="挤眼">',
        '[闭嘴]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/29/bz_thumb.gif" alt="闭嘴" title="闭嘴">',
        '[鄙视]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/71/bs2_thumb.gif" alt="鄙视" title="鄙视">',
        '[爱你]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/lovea_thumb.gif" alt="爱你" title="爱你">',
        '[泪]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9d/sada_thumb.gif" alt="泪" title="泪">',
        '[偷笑]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/19/heia_thumb.gif" alt="偷笑" title="偷笑">',
        '[亲亲]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8f/qq_thumb.gif" alt="亲亲" title="亲亲">',
        '[生病]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b6/sb_thumb.gif" alt="生病" title="生病">',
        '[太开心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/mb_thumb.gif" alt="太开心" title="太开心">',
        '[懒得理你]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/17/ldln_thumb.gif" alt="懒得理你" title="懒得理你">',
        '[右哼哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/98/yhh_thumb.gif" alt="右哼哼" title="右哼哼">',
        '[左哼哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/zhh_thumb.gif" alt="左哼哼" title="左哼哼">',
        '[嘘]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a6/x_thumb.gif" alt="嘘" title="嘘">',
        '[衰]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/cry.gif" alt="衰" title="衰">',
        '[委屈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/73/wq_thumb.gif" alt="委屈" title="委屈">',
        '[吐]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9e/t_thumb.gif" alt="吐" title="吐">',
        '[打哈气]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f3/k_thumb.gif" alt="打哈气" title="打哈气">',
        '[抱抱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/27/bba_thumb.gif" alt="抱抱" title="抱抱">',
        '[怒]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7c/angrya_thumb.gif" alt="怒" title="怒">',
        '[疑问]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5c/yw_thumb.gif" alt="疑问" title="疑问">',
        '[馋嘴]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a5/cza_thumb.gif" alt="馋嘴" title="馋嘴">',
        '[拜拜]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/88_thumb.gif" alt="拜拜" title="拜拜">',
        '[思考]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e9/sk_thumb.gif" alt="思考" title="思考">',
        '[汗]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/24/sweata_thumb.gif" alt="汗" title="汗">',
        '[困]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7f/sleepya_thumb.gif" alt="困" title="困">',
        '[睡觉]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6b/sleepa_thumb.gif" alt="睡觉" title="睡觉">',
        '[钱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/90/money_thumb.gif" alt="钱" title="钱">',
        '[失望]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0c/sw_thumb.gif" alt="失望" title="失望">',
        '[酷]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/cool_thumb.gif" alt="酷" title="酷">',
        '[花心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8c/hsa_thumb.gif" alt="花心" title="花心">',
        '[哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/49/hatea_thumb.gif" alt="哼" title="哼">',
        '[鼓掌]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/36/gza_thumb.gif" alt="鼓掌" title="鼓掌">',
        '[晕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/dizzya_thumb.gif" alt="晕" title="晕">',
        '[悲伤]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1a/bs_thumb.gif" alt="悲伤" title="悲伤">',
        '[抓狂]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/62/crazya_thumb.gif" alt="抓狂" title="抓狂">',
        '[黑线]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/h_thumb.gif" alt="黑线" title="黑线">',
        '[阴险]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/yx_thumb.gif" alt="阴险" title="阴险">',
        '[怒骂]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/nm_thumb.gif" alt="怒骂" title="怒骂">',
        '[心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/hearta_thumb.gif" alt="心" title="心">',
        '[伤心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ea/unheart.gif" alt="伤心" title="伤心">',
        '[猪头]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/pig.gif" alt="猪头" title="猪头">',
        '[ok]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d6/ok_thumb.gif" alt="ok" title="ok">',
        '[耶]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/ye_thumb.gif" alt="耶" title="耶">',
        '[good]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/good_thumb.gif" alt="good" title="good">',
        '[不要]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c7/no_thumb.gif" alt="不要" title="不要">',
        '[赞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d0/z2_thumb.gif" alt="赞" title="赞">',
        '[来]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/come_thumb.gif" alt="来" title="来">',
        '[弱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/sad_thumb.gif" alt="弱" title="弱">',
        '[蜡烛]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/lazu_thumb.gif" alt="蜡烛" title="蜡烛">',
        '[蛋糕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/cake.gif" alt="蛋糕" title="蛋糕">',
        '[钟]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d3/clock_thumb.gif" alt="钟" title="钟">',
        '[话筒]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1b/m_thumb.gif" alt="话筒" title="话筒">',
        '[玫瑰]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f6/lxhrose_org.gif" title="玫瑰" alt="玫瑰">',
        }
        textarray = re.findall("\[.+?\]", text)
        for item in textarray:
            text = text.replace(str(item),face_list[str(item)])
    except: 
        pass
    return text
