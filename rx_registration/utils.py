
from django.conf import settings

import logging

class AttrDict(dict):
    """Access a dictionary like a dict OR like a class.

    Nice little tool, taken from: http://stackoverflow.com/a/14620633
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

# these are all settings and their default values and documentation for rx-registration
rx_settings_complete = {
    'token_length': (12, 'The length of the confirmation tokens.'),
    'confirm_registration': (True, 'Do you want to send newly-registered users an email for confirmation?'),
    'confirm_registration_from': ('', 'The email name/address that gets put into the FROM name for sending emails.'),
    'redirect_after_register': ('/', 'Where should we redirect the user to after registering? (URL oder urlconf name)'),
    'redirect_after_login': ('/', 'Where should we redirect the user to after logging in? (URL oder urlconf name)'),
    'redirect_after_logout': ('/', 'Where should we redirect the user to after logging out? (URL oder urlconf name)'),
}

rxsettings = AttrDict({k: v[0] for k, v in rx_settings_complete.items()})
rxsettings_documentation = {k: v[1] for k, v in rx_settings_complete.items()}

try:
    rxsettings.update(settings.RX_REGISTRATION_SETTINGS)
except AttributeError:
    logging.warning('Could not find `settings.RX_REGISTRATION_SETTINGS`, used all defaults instead.')
except TypeError:
    logging.error('Setting `settings.RX_REGISTRATION_SETTINGS` is not a dictionary, MUST be one. Is {} instead.'.format(
        type(settings.RX_REGISTRATION_SETTINGS),
    ))




