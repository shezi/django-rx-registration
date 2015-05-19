"""
A user registration app that makes it easy for you!
"""

from django.apps import AppConfig


class RxRegAppConfig(AppConfig):
    name = 'rx-registration'
    verbose_name = "Rx-Registration"


default_app_config = 'rx-registration.RxRegAppConfig'