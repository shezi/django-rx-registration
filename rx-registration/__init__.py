"""
A user registration app that makes it easy for you!
"""

__version__ = '0.1.0'


from django.apps import AppConfig


class RxRegAppConfig(AppConfig):
    name = 'rx-registration'
    verbose_name = "Rx-Registration"


default_app_config = 'rx-registration.RxRegAppConfig'