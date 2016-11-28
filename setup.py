import os
from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()


setup(name='oidc_custom_provider',
      version='0.1',
      description='Custom OIDC provider using Google OAuth example',
      url='https://github.com/hrvojevu/custom_oidc_provider',
      author='ExtensionEngine',
      author_email='hvucic@extensionengine.com',
      long_description=README,
      license='MIT',
      packages=['oidc_custom_provider'],
      zip_safe=False)