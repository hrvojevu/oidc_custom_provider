from social.backends.oauth import BaseOAuth2


class BaseGoogleAuth(object):
    def get_user_id(self, details, response):
        """Use google email as unique id"""
        if self.setting('USE_UNIQUE_USER_ID', False):
            return response['id']
        else:
            return details['email']

    def get_user_details(self, response):
        """Return user details from Google API account"""
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


class BaseGoogleOAuth2API(BaseGoogleAuth):
    def get_scope(self):
        """Return list with needed access scope"""
        scope = self.setting('SCOPE', [])
        if not self.setting('IGNORE_DEFAULT_SCOPE', False):
            default_scope = []
            if self.setting('USE_DEPRECATED_API', False):
                default_scope = self.DEPRECATED_DEFAULT_SCOPE
            else:
                default_scope = self.DEFAULT_SCOPE
            scope = scope + (default_scope or [])
        return scope

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        if self.setting('USE_DEPRECATED_API', False):
            url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        else:
            url = 'https://www.googleapis.com/plus/v1/people/me'
        return self.get_json(url, params={
            'access_token': access_token,
            'alt': 'json'
        })

    def revoke_token_params(self, token, uid):
        return {'token': token}

    def revoke_token_headers(self, token, uid):
        return {'Content-type': 'application/json'}


class CustomGoogleOAuth2(BaseGoogleOAuth2API, BaseOAuth2):
    """Google OAuth2 authentication backend"""
    name = 'custom-google-oauth2'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    # The order of the default scope is important
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
    DEPRECATED_DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]
