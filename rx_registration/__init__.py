"""
A user registration app that makes it easy for you!
"""

from django.apps import AppConfig


__version__ = '0.1.0'


class RxRegAppConfig(AppConfig):
    name = 'rx_registration'
    verbose_name = "Rx-Registration"


default_app_config = 'rx_registration.RxRegAppConfig'
