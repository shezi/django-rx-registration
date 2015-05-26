from django.db import models
from django.conf import settings

from django.utils.translation import ugettext as _


class SignupConfirmationToken(models.Model):
    """
    A confirmation token for newly-registered users.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        help_text=_(''),
    )

    token_hash = models.CharField(
        max_length=32, editable=False,
        verbose_name=_('Token hash'),
        help_text=_('A password hash of the actual token (for security).'),
    )

    expires = models.DateTimeField(
        verbose_name=_('Expires'),
        help_text=_(''),
    )

    used = models.DateTimeField(
        blank=True, null=True, editable=False,
        verbose_name=_('Used'),
        help_text=_(''),
    )

    class Meta:
        verbose_name = _('Signup confirmation token')
        verbose_name_plural = _('Signup confirmation tokens')


class PasswordResetToken(models.Model):
    """
    A token for resetting a password.

    Since these tokens are just as good as passwords, the same safety standards apply and the same care should be taken
    when handling them.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        help_text=_(''),
    )

    token_hash = models.CharField(
        editable=False,
        max_length=32,
        verbose_name=_('Token hash'),
        help_text=_('A password hash of the actual token (for security).'),
    )

    expires = models.DateTimeField(
        verbose_name=_('Expires'),
        help_text=_(''),
    )

    used = models.DateTimeField(
        blank=True, null=True, editable=False,
        verbose_name=_('Used'),
        help_text=_(''),
    )

    class Meta:
        verbose_name = _('Password reset token')
        verbose_name_plural = _('Password reset tokens')

