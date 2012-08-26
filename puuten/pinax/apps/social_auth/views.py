#coding=utf-8
"""Views

Notes:
    * Some views are marked to avoid csrf tocken check because they rely
      on third party providers that (if using POST) won't be sending csrf
      token back.
"""
from __future__ import division
from functools import wraps
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
#by jipan from django.contrib import messages
from importlib import import_module
#by jipan from django.views.decorators.csrf import csrf_exempt

from social_auth.backends import get_backend
from social_auth.utils import sanitize_redirect, setting, log, \
                              backend_setting, clean_partial_pipeline

from social_auth.backends.weibo import APIClient
from social_auth.models  import UserSocialAuth
from business_sina.models import * 
from datetime import datetime
import email.utils
from django.utils.encoding import smart_str, smart_unicode
from business_sina_weibo.models import WeiBo as SinaWeiBo, WeiBo_ImportConfig
import re
import sys
import Image
import urllib
import os


DEFAULT_REDIRECT = setting('SOCIAL_AUTH_LOGIN_REDIRECT_URL') or \
                   setting('LOGIN_REDIRECT_URL')
LOGIN_ERROR_URL = setting('LOGIN_ERROR_URL', setting('LOGIN_URL'))
RAISE_EXCEPTIONS = setting('SOCIAL_AUTH_RAISE_EXCEPTIONS', setting('DEBUG'))
PROCESS_EXCEPTIONS = setting('SOCIAL_AUTH_PROCESS_EXCEPTIONS',
                             'social_auth.utils.log_exceptions_to_messages')


def dsa_view(redirect_name=None):
    """Decorate djangos-social-auth views. Will check and retrieve backend
    or return HttpResponseServerError if backend is not found.

        redirect_name parameter is used to build redirect URL used by backend.
    """
    def dec(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            if redirect_name:
                redirect = reverse(redirect_name, args=(backend,))
            else:
                redirect = request.path
            backend = get_backend(backend, request, redirect)

            if not backend:
                return HttpResponseServerError('Incorrect authentication ' + \
                                               'service')

            try:
                return func(request, backend, *args, **kwargs)
            except Exception, e:  # some error ocurred
                if RAISE_EXCEPTIONS:
                    raise
                log('error', unicode(e), exc_info=True, extra={
                    'request': request
                })

                mod, func_name = PROCESS_EXCEPTIONS.rsplit('.', 1)
                try:
                    process = getattr(import_module(mod), func_name,
                                      lambda *args: None)
                except ImportError:
                    pass
                else:
                    process(request, backend, e)

                url = backend_setting(backend, 'SOCIAL_AUTH_BACKEND_ERROR_URL',
                                      LOGIN_ERROR_URL)
                return HttpResponseRedirect(url)
        return wrapper
    return dec


@dsa_view(setting('SOCIAL_AUTH_COMPLETE_URL_NAME', 'socialauth_complete'))
def auth(request, backend):
    """Start authentication process"""
    return auth_process(request, backend)


#@csrf_exempt
@dsa_view()
def complete(request, backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return complete_process(request, backend, *args, **kwargs)


@login_required
@dsa_view(setting('SOCIAL_AUTH_ASSOCIATE_URL_NAME',
                  'socialauth_associate_complete'))
def associate(request, backend):
    """Authentication starting process"""
    return auth_process(request, backend)


#@csrf_exempt
@login_required
@dsa_view()
def associate_complete(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, request.user, *args, **kwargs)

    if not user:
        url = backend_setting(backend, 'LOGIN_ERROR_URL', LOGIN_ERROR_URL)
    elif isinstance(user, HttpResponse):
        return user
    else:
        url = backend_setting(backend,
                              'SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL') or \
              redirect_value or \
              DEFAULT_REDIRECT
    print user
    print url
    return HttpResponseRedirect(url)


@login_required
@dsa_view()
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    backend.disconnect(request.user, association_id)
    url = request.REQUEST.get(REDIRECT_FIELD_NAME, '') or \
          backend_setting(backend, 'SOCIAL_AUTH_DISCONNECT_REDIRECT_URL') or \
          DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


def auth_process(request, backend):
    """Authenticate using social backend"""
    # Save any defined next value into session
    data = request.POST if request.method == 'POST' else request.GET
    if REDIRECT_FIELD_NAME in data:
        # Check and sanitize a user-defined GET/POST next field value
        redirect = data[REDIRECT_FIELD_NAME]
        if setting('SOCIAL_AUTH_SANITIZE_REDIRECTS', True):
            redirect = sanitize_redirect(request.get_host(), redirect)
        request.session[REDIRECT_FIELD_NAME] = redirect or DEFAULT_REDIRECT

    # Clean any partial pipeline info before starting the process
    clean_partial_pipeline(request)

    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def complete_process(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, *args, **kwargs)
    print user
    if isinstance(user, HttpResponse):
        return user

    if not user and request.user.is_authenticated():
        return HttpResponseRedirect(redirect_value)

    if user:
        if getattr(user, 'is_active', True):
            login(request, user)
            # user.social_user is the used UserSocialAuth instance defined
            # in authenticate process
            social_user = user.social_user
            if redirect_value:
                request.session[REDIRECT_FIELD_NAME] = redirect_value or \
                                                       DEFAULT_REDIRECT

            if setting('SOCIAL_AUTH_SESSION_EXPIRATION', True):
                # Set session expiration date if present and not disabled by
                # setting. Use last social-auth instance for current provider,
                # users can associate several accounts with a same provider.
                if social_user.expiration_delta():
                    request.session.set_expiry(social_user.expiration_delta())

            # store last login backend name in session
            key = setting('SOCIAL_AUTH_LAST_LOGIN',
                          'social_auth_last_login_backend')
            request.session[key] = social_user.provider

            # Remove possible redirect URL from session, if this is a new
            # account, send him to the new-users-page if defined.
            new_user_redirect = backend_setting(backend,
                                           'SOCIAL_AUTH_NEW_USER_REDIRECT_URL')
            if new_user_redirect and getattr(user, 'is_new', False):
                url = new_user_redirect
            else:
                url = redirect_value or \
                      backend_setting(backend,
                                      'SOCIAL_AUTH_LOGIN_REDIRECT_URL') or \
                      DEFAULT_REDIRECT
        else:
            url = backend_setting(backend, 'SOCIAL_AUTH_INACTIVE_USER_URL',
                                  LOGIN_ERROR_URL)
    else:
        msg = setting('LOGIN_ERROR_MESSAGE', None)
        if msg:
            print "messages.error(request, msg)".join(msg)
        url = backend_setting(backend, 'LOGIN_ERROR_URL', LOGIN_ERROR_URL)
    return HttpResponseRedirect(url)


def auth_complete(request, backend, user=None, *args, **kwargs):
    """Complete auth process. Return authenticated user or None."""
    if user and not user.is_authenticated():
        user = None

    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    if request.session.get(name):
        data = request.session.pop(name)
        idx, args, kwargs = backend.from_session_dict(data, user=user,
                                                      request=request,
                                                      *args, **kwargs)
        return backend.continue_pipeline(pipeline_index=idx, *args, **kwargs)
    else:
        return backend.auth_complete(user=user, request=request, *args,
                                     **kwargs)


#WEIBO_APP_ID                     = setting('WEIBO_APP_ID')#'3379939141'
#WEIBO_API_SECRET                 = setting('WEIBO_API_SECRET')#'4741cf0918a8625eae02ab6ac297c375'
WEIBO_APP_ID                     = '3379939141'
WEIBO_API_SECRET                 = '4741cf0918a8625eae02ab6ac297c375'

REDIRECT_URL                     = 'http://www.puuter.com/auth/commplete/'

  

def updateSinaBSInfos(useridinweibo, myuser, client):
    weibouserids = []
    next_cursor = 0
    INIT = True
    pagecount = 200
    
    while INIT or next_cursor > 0:
        INIT = False
        friends = client.get.friendships__friends(uid=useridinweibo, cursor=next_cursor, count=pagecount)
        next_cursor = friends.next_cursor 
       
        #print total_number,next_cursor
       
        for bsina in friends.users:
            #bsina = client.get.users__show(uid=one.id)
            #print bsina.id,bsina.screen_name
            weibouserids.append(bsina.id)
            try:
                bsina_puuter = BSInfo.objects.get(sina_id=bsina.id)
            except:
                bsina_puuter = None
            if bsina_puuter is None:
                bsina_puuter = BSInfo(sina_id=bsina.id)
            bsina_puuter.name = bsina.screen_name
            if bsina.domain is None or bsina.domain == "":
                bsina.domain = str(bsina.id)
            bsina_puuter.sina_url = "http://weibo.com/" + bsina.domain
            bsina_puuter.location = bsina.location
            bsina_puuter.followed_by_id = useridinweibo
            bsina_puuter.introduction = bsina.description
            bsina_puuter.avatar = bsina.profile_image_url
            bsina_puuter.avatar_large = bsina.avatar_large
            bsina_puuter.p_or_b = getPersionOrBusiness(bsina.verified_reason)
            bsina_puuter.varified_or_not = bsina.verified
            bsina_puuter.updated_at = datetime.now()
            bsina_puuter.created_by = myuser.user
            bsina_puuter.save()
    #print weibouserids
    return weibouserids#,output

MAX_SINA_BATCH_TAGS = 20

def updateSinaBSinfoTags(client, weibouserids):
    uidsstr = ''
    for i in range(len(weibouserids)):
        uidsstr += str(weibouserids[i]) + ','
        if (i+1) % MAX_SINA_BATCH_TAGS == 0:
            #print uidsstr[:-1]
            updateBSInfoTags(client, uidsstr[:-1])
            uidsstr = ''
    
    if len(uidsstr) > 1:
        updateBSInfoTags(client, uidsstr[:-1])

def importbusiness(request, useridinweibo = "2734461097" , *args, **kwargs):
    
    myuser = UserSocialAuth.objects.get(provider='weibo',uid=useridinweibo)    
    expires_in    = UserSocialAuth.expires(myuser)# token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    access_token = myuser.tokens['access_token']# 新浪返回的token，类似abc123xyz456
    #print access_token,expires_in
    client = APIClient(app_key=WEIBO_APP_ID, app_secret=WEIBO_API_SECRET, redirect_uri=REDIRECT_URL)
    #print client.request_access_token_use_password(username="wjl.abc@hotmail.com",password="5663131")
    
    client.set_access_token(access_token, expires_in)

    weibouserids = updateSinaBSInfos(useridinweibo, myuser, client)
    
    updateSinaBSinfoTags(client, weibouserids)  
        
    return HttpResponse("导入成功"+str(useridinweibo) ) 


def updateBSInfoTags(client,uids_str):
    tagsData = client.get.tags__tags_batch(uids = uids_str)
    for user in tagsData:
        try:
            bsina_puuter = BSInfo.objects.get(sina_id=user.id) 
            bsina_puuter.tags = getUserTags(user.tags)
            bsina_puuter.updated_at = datetime.now()
            bsina_puuter.save()
        except:
            continue
        
    

def getUserTags(tags):
    result = ""
    for tag in tags:
        for tkey in tag.keys():
            if tkey != 'weight':
                result += (' ' + tag[tkey])
    return result

def getPersionOrBusiness(reason):
    #print smart_str(reason)
    #print smart_str(reason)
    return 2


def import_weibo(request, useridinweibo = "2734461097" , *args, **kwargs):
    
    myuser = UserSocialAuth.objects.get(provider='weibo',uid=useridinweibo)    
    expires_in    = UserSocialAuth.expires(myuser)# token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    access_token = myuser.tokens['access_token']# 新浪返回的token，类似abc123xyz456
    #print access_token,expires_in
    client = APIClient(app_key=WEIBO_APP_ID, app_secret=WEIBO_API_SECRET, redirect_uri=REDIRECT_URL)
    client.set_access_token(access_token, expires_in)
    try: 
        importConfig = WeiBo_ImportConfig.objects.get(sina_uid=useridinweibo)
    except:
        print "Unexpected error:", sys.exc_info()
        importConfig = WeiBo_ImportConfig(sina_uid=useridinweibo,sina_weiboid=0)
    try:
        updateSinaWeiBos(useridinweibo, myuser, client,importConfig)
    except:
        print "Unexpected error:", sys.exc_info()
        importConfig.save()
    return HttpResponse("导入成功"+str(useridinweibo) ) 
import shutil
 

def updateSinaWeiBos(useridinweibo, myuser, client, importConfig):
    next_cursor = 0
    since_cursor = importConfig.sina_weiboid
    pagecount = 100
    condition = True
    pagenum = 1
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT,'sina_pic_temp')) :
        os.makedirs(os.path.join(settings.MEDIA_ROOT,'sina_pic_temp'))
    while condition :
        friends_timeline = client.get.statuses__home_timeline(page=pagenum, count=pagecount)
        next_cursor = friends_timeline.next_cursor
        print friends_timeline.previous_cursor,friends_timeline.next_cursor
        for weibo in friends_timeline.statuses:
            #print weibo.created_at,weibo.mid,weibo.text,weibo
            print weibo.id
            if importConfig.sina_weiboid < weibo.id:
                importConfig.sina_weiboid = weibo.id
            
            try:
                sina_weibo = SinaWeiBo.objects.get(sina_id=weibo.id)
                continue
            except:
                sina_weibo = getSinaWeiBo(weibo)                
                sina_weibo_retweeted = None
                if hasattr(weibo,'retweeted_status'):
                    sina_weibo.retweeted_sina_id = weibo.retweeted_status.id
                    try:
                        sina_weibo_retweeted = SinaWeiBo.objects.get(sina_id=sina_weibo.retweeted_sina_id)
                    except:
                        sina_weibo_retweeted = getSinaWeiBo(weibo.retweeted_status)
                        #isSaveWeibo = save_Weibo(sina_weibo_retweeted)
                save_Weibo(sina_weibo,sina_weibo_retweeted)
                """
                isSaveWeibo = save_Weibo(sina_weibo,isSaveWeibo) 
                if sina_weibo.retweeted_sina_id != None :                    
                    sina_weibo_retweeted.status = "99"
                    save_Weibo(sina_weibo_retweeted,isSaveWeibo)
                """
            if since_cursor >= weibo.id or next_cursor==0:
                condition = False
                break
        pagenum = pagenum + 1
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT,'sina_pic_temp'))
    importConfig.save()
    
ACCEPTED_ASPECT_RATIO = 5.5    
    
def save_Weibo(sina_weibo,sina_weibo_retweeted):
    print sina_weibo.sina_id, sina_weibo.status
    if sina_weibo_retweeted is None:
        if (sina_weibo.status != '4' and sina_weibo.thumbnail_pic != None and check_WeiBo_Value(sina_weibo.reposts_count,sina_weibo.comments_count)):
            sina_weibo.status = '5'
        if(check_WeiBo_Text_NotSaved(sina_weibo.sina_text) or sina_weibo.aspect_ratio>ACCEPTED_ASPECT_RATIO):
            return None
        if sina_weibo.status == '4' or sina_weibo.status == '5'  :        
            sina_weibo.save()
    else :   
        set_WeiBo_Status_Again(sina_weibo,sina_weibo_retweeted)            
        if sina_weibo.status == '4' or sina_weibo.status == '5' or sina_weibo.status == '6':     
            sina_weibo.save() 
            sina_weibo_retweeted.save()
    
def getSinaWeiBo(weibo):
    sweibo = SinaWeiBo(sina_id=weibo.id,sina_text=weibo.text)
    if weibo.created_at is not None and weibo.created_at != '':
        sweibo.created_at=datetime(*email.utils.parsedate_tz(weibo.created_at)[:6])
    #datetime.strptime(weibo.created_at,'%a %b %d %H:%M:%S %z %Y') )
    if hasattr(weibo,'annotations'):
        sweibo.annotations=str(weibo.annotations)
    if hasattr(weibo,'original_pic'):
        sweibo.original_pic=weibo.original_pic
    if hasattr(weibo,'thumbnail_pic'):
        sweibo.thumbnail_pic= weibo.thumbnail_pic
        sweibo.aspect_ratio = get_Pic_Aspect_Ratio(weibo.thumbnail_pic)
    else :
        sweibo.aspect_ratio = 1 #所有头像默认比例为1
    if hasattr(weibo,'bmiddle_pic'):
        sweibo.bmiddle_pic=weibo.bmiddle_pic
    if hasattr(weibo,'avatar_large'):
        sweibo.avatar_large=weibo.avatar_large
    if hasattr(weibo,'reposts_count'):
        sweibo.reposts_count=weibo.reposts_count
    if hasattr(weibo,'comments_count'):
        sweibo.comments_count=weibo.comments_count
    if hasattr(weibo,'source'):
        sweibo.source=weibo.source
    if hasattr(weibo,'geo'):
        sweibo.sina_geo=str(weibo.geo)
    if hasattr(weibo,'user'):
        sweibo.sina_user=json.dumps(weibo.user)
        sweibo.sina_userid=weibo.user.id
    set_WeiBo_Status(sweibo)
    return sweibo


def get_Pic_Aspect_Ratio(url):
    try:
        fname = os.path.join(os.path.join(settings.MEDIA_ROOT,"sina_pic_temp"), url.split('/')[-1])
        urllib.urlretrieve(url,fname)
        img = Image.open(fname,"r")
        width,height =  img.size
        img.save(fname,img.format)        
    except :
        print "get_Pic_Aspect_Ratio save error:", sys.exc_info()
        return ACCEPTED_ASPECT_RATIO+1
    try:
        os.remove(fname)
    except :
        print "get_Pic_Aspect_Ratio delete error:", sys.exc_info()
        return ACCEPTED_ASPECT_RATIO+1
    return height/width

def delete_BSInfo_Friendships(BSInfo_sinaid,BSInfo_followed_by_id):
    myuser = UserSocialAuth.objects.get(provider='weibo',uid=BSInfo_followed_by_id)
    expires_in    = UserSocialAuth.expires(myuser)# token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    access_token = myuser.tokens['access_token']# 新浪返回的token，类似abc123xyz456
    client = APIClient(app_key=WEIBO_APP_ID, app_secret=WEIBO_API_SECRET, redirect_uri=REDIRECT_URL)
    client.set_access_token(access_token, expires_in)    
    try:
        result = not client.post.friendships__destroy(uid=BSInfo_sinaid).following
    except:
        result = not client.get.friendships__show(source_id=BSInfo_followed_by_id,target_id=BSInfo_sinaid).target.following
    return result

def check_WeiBo_Status(text):
    if re.search(u'(\d+)(?:日|元|号)',text) or re.search(u'(\d+)\.(\d+)',text) \
         or re.search(u'(\d+)\/(\d+)',text) \
         or re.search(u'(?:明天|今天|后天|今晚|明晚|优惠|折扣|促销|折)',text) \
         or re.search(u'(?:周|星期|礼拜)(?:一|二|三|四|五|六|日|天)',text) :
        return True
    else:
        return False
    
def set_WeiBo_Status(sina_weibo):
    if check_WeiBo_Status(sina_weibo.sina_text):
        sina_weibo.status = '4'
    elif (sina_weibo.status != '4' and sina_weibo.thumbnail_pic != None and check_WeiBo_Value(sina_weibo.reposts_count,sina_weibo.comments_count)):
        sina_weibo.status = '5'
    else :
        sina_weibo.status = '1'
    if(check_WeiBo_Text_NotSaved(sina_weibo.sina_text) or sina_weibo.aspect_ratio>ACCEPTED_ASPECT_RATIO):
        sina_weibo.status = '-1'   
        
def set_WeiBo_Status_Again(sina_weibo,sina_weibo_retweeted):
    if sina_weibo.status != '4' and sina_weibo_retweeted.status > 0 :
        sina_weibo.status = sina_weibo_retweeted.status
    if sina_weibo_retweeted.thumbnail_pic != None :
        sina_weibo.aspect_ratio = sina_weibo_retweeted.aspect_ratio
        if check_WeiBo_Text_Personal(sina_weibo,sina_weibo_retweeted) :
            sina_weibo.status = '6'
    if sina_weibo.status == '4' or sina_weibo.status == '5' or sina_weibo.status == '6':
        sina_weibo_retweeted.status = '99'
        
def check_WeiBo_Text_Personal(sina_weibo,sina_weibo_retweeted):
    if sina_weibo.sina_userid == sina_weibo_retweeted.sina_userid:
        return False
    if re.search(u'@('+json.loads(sina_weibo.sina_user)['name']+')',sina_weibo_retweeted.sina_text) or \
        re.search(u'@('+json.loads(sina_weibo.sina_user)['screen_name']+')',sina_weibo_retweeted.sina_text):
        return True
    else:
        return False

def check_WeiBo_Value(reposts_count,comments_count):
    if comments_count <50 and reposts_count <50 and (reposts_count > 0 and comments_count >0 and abs(reposts_count - comments_count)<11) :
        return True
    else:
        return False
    
def check_WeiBo_Text_NotSaved(text):
    if re.search(u'#(?:晚安|语|相册|分享|推荐|歌星|健康|明星|微薄|问候|早安|时尚|中国|清晨|快递)#',text) :
        return True
    else:
        return False