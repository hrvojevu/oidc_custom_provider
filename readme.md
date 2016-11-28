OIDC Custom provider
=======================

Installation
------------

Installation is modular. Install using pip, from this repository:

```bash
$ pip install git+https://github.com/hrvojevu/oidc_custom_provider
```
After installing, import this package and add this provider to AUTHENTICATION_BACKENDS inside /edx-platform/lms/envs/aws.py:

```bash
import oidc_custom_provider

AUTHENTICATION_BACKENDS = (
    ENV_TOKENS.get('THIRD_PARTY_AUTH_BACKENDS', [
        'social.backends.google.GoogleOAuth2',
        'social.backends.linkedin.LinkedinOAuth2',
        'social.backends.facebook.FacebookOAuth2',
        'social.backends.azuread.AzureADOAuth2',
        'third_party_auth.saml.SAMLAuthBackend',
        'third_party_auth.lti.LTIAuthBackend',
        'oidc_custom_provider.provider.CustomOAuth2',
    ]) + list(AUTHENTICATION_BACKENDS)
)
```

License
-------

The MIT License (MIT)
Copyright (c) 2016 ExtensionEngine, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
