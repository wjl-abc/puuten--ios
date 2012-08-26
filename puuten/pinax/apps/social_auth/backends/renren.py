"""
RenRen OAuth support.

This contribution adds support for RenRen OAuth service. The settings
RenRen_APP_ID and RenRen_API_SECRET must be defined with the values
given by RenRen application registration process.

Extended permissions are supported by defining RenRen_EXTENDED_PERMISSIONS
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


# RenRen configuration
#RENREN_ME = 'https://graph.facebook.com/me?'
ACCESS_TOKEN = 'http://graph.renren.com/oauth/token?'


class RenRenBackend(OAuthBackend):
    """RenRen OAuth2 authentication backend"""
    name = 'renren'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('refresh_token', 'refresh_token', True),
        ('expires_in', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from RenRen account"""
        return {USERNAME: response.get('name'),
                'email': response.get('email', ''),
                'fullname': response.get('name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}


class RenRenAuth(BaseOAuth2):
    """RENREN OAuth2 support"""
    AUTH_BACKEND = RenRenBackend
    #RESPONSE_TYPE = None
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = 'http://graph.renren.com/oauth/authorize'
    SETTINGS_KEY_NAME = 'RENREN_APP_ID'
    SETTINGS_SECRET_NAME = 'RENREN_API_SECRET'
    RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
    RENREN_API_SERVER = "http://api.renren.com/restserver.do"

    def get_scope(self):
        return setting('RENREN_EXTENDED_PERMISSIONS', [])

 
    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' not in self.data:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)
        url = ACCESS_TOKEN + urlencode({
            'grant_type': 'authorization_code',
            'client_id': setting('RENREN_APP_ID'),
            'redirect_uri': self.redirect_uri,
            'client_secret': setting('RENREN_API_SECRET'),
            'code': self.data['code']
        })
        try:
            print self.AUTH_BACKEND.name,url
            res = urlopen(url).read()
            response = simplejson.loads(res)
        except HTTPError:
            raise AuthFailed(self, 'There was an error authenticating the app')
     
        access_token = response['access_token']
        data = response['user']
        
        if data is not None:
            data['access_token'] = access_token
            data['id'] = str(data['id'])
            data['email'] = data['id']+'@renren'
            # expires will not be part of response if offline access
            # premission was requested
            if 'expires_in' in response:
                data['expires_in'] = response['expires_in']
                
            if 'refresh_token' in response:
                data['refresh_token'] = response['refresh_token']                
        
        kwargs.update({'auth': self,
                       'response': data,
                       'username': data['id'] ,
                       self.AUTH_BACKEND.name: True})
        print data
        return authenticate(*args, **kwargs)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return setting('RENREN_APP_ID') and setting('RENREN_API_SECRET')


# Backend definition
BACKENDS = {
    'renren': RenRenAuth,
}
