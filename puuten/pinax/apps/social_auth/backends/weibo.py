#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.04'
__author__ = 'Liao Xuefeng (askxuefeng@gmail.com)'

'''
Python client SDK for sina weibo API using OAuth 2.
'''

try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import logging
"""
WeiBo OAuth support.

This contribution adds support for WeiBo OAuth service. The settings
WeiBo_APP_ID and WeiBo_API_SECRET must be defined with the values
given by WeiBo application registration process.

Extended permissions are supported by defining WeiBo_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import cgi
from urllib import urlencode
from urllib2 import urlopen, HTTPError

from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import sanitize_log_data, setting, log
from social_auth.backends.exceptions import AuthException, AuthCanceled, \
                                            AuthFailed, AuthTokenError


# WeiBo configuration
#WEIBO_ME = 'https://graph.facebook.com/me?'
ACCESS_TOKEN = 'http://api.weibo.com/oauth/token?'


class WeiBoBackend(OAuthBackend):
    """WeiBo OAuth2 authentication backend"""
    name = 'weibo'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('refresh_token', 'refresh_token', True),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from WeiBo account"""
        return {USERNAME: response.get('name'),
                'email': response.get('email', ''),
                'fullname': response.get('name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}


class WeiBoAuth(BaseOAuth2):
    """WEIBO OAuth2 support"""
    AUTH_BACKEND = WeiBoBackend
    #RESPONSE_TYPE = None
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = 'http://api.weibo.com/oauth2/'
    SETTINGS_KEY_NAME = 'WEIBO_APP_ID'
    SETTINGS_SECRET_NAME = 'WEIBO_API_SECRET'
    

    def get_scope(self):
        return setting('WEIBO_EXTENDED_PERMISSIONS', [])

    def auth_url(self):
        client = APIClient(app_key=setting('WEIBO_APP_ID'), app_secret=setting('WEIBO_API_SECRET'), redirect_uri=self.redirect_uri)
        return client.get_authorize_url()
    
    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' not in self.data:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)
        # 获取URL参数code:
        code = self.data['code']
        client = APIClient(app_key=setting('WEIBO_APP_ID'), app_secret=setting('WEIBO_API_SECRET'), redirect_uri=self.redirect_uri)
        r = client.request_access_token(code)
        access_token = r.access_token # 新浪返回的token，类似abc123xyz456
        expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        # TODO: 在此可保存access token
        client.set_access_token(access_token, expires_in) 
        #access_token = response['access_token']
        data = r.copy()
        if data is not None:
            data['access_token'] = r.access_token
            data['id'] = r.uid
            data['email'] = r.uid+'@weibo'
            # expires will not be part of response if offline access
            # premission was requested
            if 'expires_in' in r:
                data['expires'] = r['expires_in']
                
            if 'refresh_token' in r:
                data['refresh_token'] = r['refresh_token']
        kwargs.update({'auth': self,
                       'response': data,
                       'username': r.uid ,
                       self.AUTH_BACKEND.name: True})
        return authenticate(*args, **kwargs)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return setting('WEIBO_APP_ID') and setting('WEIBO_API_SECRET')


# Backend definition
BACKENDS = {
    'weibo': WeiBoAuth,
}
def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_call(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_call(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('MULTIPART POST %s' % url)
    return _http_call(url, _HTTP_UPLOAD, authorization, **kw)

def _http_call(url, method, authorization, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method==_HTTP_GET else url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib2.urlopen(req)
    body = resp.read()
    r = json.loads(body, object_hook=_obj_hook)
    if hasattr(r, 'error_code'):
        raise APIError(r.error_code, getattr(r, 'error', ''), getattr(r, 'request', ''))
    return r

class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.access_token, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.auth_url, 'authorize', \
                _encode_params(client_id = self.client_id, \
                        response_type = 'code', \
                        display = display, \
                        redirect_uri = redirect))

    def request_access_token_use_password(self,username="wjl.abc@hotmail.com",password="5663131"):
        r = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret,\
                grant_type = 'password',username=username,password=password)
        r.expires_in += int(time.time())
        return r
        
      
        
    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        r = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                redirect_uri = redirect, \
                code = code, grant_type = 'authorization_code')
        r.expires_in += int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)
