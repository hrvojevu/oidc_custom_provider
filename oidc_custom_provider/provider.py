from social.backends.oauth import BaseOAuth2
import logging
import ssl
import base64

class BaseOIDCAuth(object):
    def get_user_id(self, details, response):
        if self.setting('USE_UNIQUE_USER_ID', False):
            return response['id']
        else:
            return details['email']

    def get_user_details(self, response):
        if 'email' in response:
            email = response['email']
        elif 'emails' in response:
            email = response['emails'][0]['value']
        else:
            email = ''

        if isinstance(response.get('name'), dict):
            names = response.get('name') or {}
            name, given_name, family_name = (
                response.get('displayName', ''),
                names.get('givenName', ''),
                names.get('familyName', '')
            )
        else:
            name, given_name, family_name = (
                response.get('name', ''),
                response.get('given_name', ''),
                response.get('family_name', '')
            )

        fullname, first_name, last_name = self.get_user_names(
            name, given_name, family_name
        )
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}


class BaseOAuth2API(BaseOIDCAuth):
    def get_scope(self):
        """Return list with needed access scope"""
        scope = self.setting('SCOPE', [])
        if not self.setting('IGNORE_DEFAULT_SCOPE', False):
            scope = scope + (self.DEFAULT_SCOPE or [])
        return scope

    def user_data(self, access_token, *args, **kwargs):
        url = 'https://oidc.tex.extensionengine.com/op/me'
        return self.get_json(url , headers={
            'Authorization': 'Bearer {0}'.format(access_token)
        })

    def revoke_token_params(self, token, uid):
        return {'token': token}

    def revoke_token_headers(self, token, uid):
        return {'Content-type': 'application/json'}


class CustomOAuth2(BaseOAuth2API, BaseOAuth2):
    name = 'oidc-oauth2'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://oidc.tex.extensionengine.com/op/auth'
    ACCESS_TOKEN_URL = 'https://oidc.tex.extensionengine.com/op/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = 'https://oidc.tex.extensionengine.com/op/token/revocation'
    REVOKE_TOKEN_METHOD = 'GET'
    # The order of the default scope is important
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True),
        ('prompt', 'consent')
    ]
    SSL_PROTOCOL = ssl.PROTOCOL_TLSv1

    def auth_headers(self):
        client_id, client_secret = self.get_key_and_secret()
        return {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'Authorization': 'Basic {0}='.format(base64.b64encode(client_id + ':' + client_secret))}

    def auth_complete_params(self, state=None):
        return {
            'grant_type': 'authorization_code',  # request auth code
            'code': self.data.get('code', ''),  # server response code
            'redirect_uri': self.get_redirect_uri(state)
        }
