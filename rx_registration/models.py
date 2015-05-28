
import random
from datetime import timedelta

from django.db import models
from django.conf import settings

from django.contrib.auth.hashers import check_password, make_password

from django.utils.translation import ugettext as _
from django.utils import timezone

from .utils import rxsettings

# these are characters that cannot be mistaken for other characters
ALPHABET = 'ACDEFGHKLMNPRSTWXYZ2345679'

def create_token_password(length=rxsettings.token_length):

    return ''.join(
        (random.choice(ALPHABET) for _ in range(length))
    )


class SignupConfirmationToken(models.Model):
    """
    A confirmation token for newly-registered users.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        help_text=_(''),
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        help_text=_('The email address that is being verified with this token.'),
    )

    token_id = models.CharField(
        max_length=128,
        verbose_name=_('Token ID'),
        help_text=_('The token id used for looking up the correct token.'),
    )

    token_hash = models.CharField(
        max_length=128,
        verbose_name=_('Token hash'),
        help_text=_('A password hash of the actual token (for security).'),
    )

    expires = models.DateTimeField(
        verbose_name=_('Expires'),
        help_text=_(''),
    )

    used = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('Used'),
        help_text=_(''),
    )

    @classmethod
    def make_token(cls, user, email, expires_in=86400):
        """
        Make a token for a given user/email combination and return the token password and the saved token itself.

        You will get two return values: the token password as well as the saved token object. The token password
        can NOT be recovered from the saved token object, so don't lose it!
        Note that `token.token_id` is necessary to verify the token, so send that to the user as well!

        Tokens will get created with the `create_token_password` method in this module.
        The `expires_in` parameters determines in how many seconds this token will expire and won't be useable any more.
        """
        password = create_token_password()
        password_hash = make_password(password)

        token = cls.objects.create(
            token_id=create_token_password(),
            user=user, email=email,
            token_hash=password_hash,
            expires=timezone.now() + timedelta(seconds=expires_in)
        )

        return password, token

    @classmethod
    def check_token(cls, token_id, token_password):
        """
        Check a token password against the currently available tokens. Spaces and dashes will be ignored.

        Will return the token if the password is valid or None otherwise.
        """
        token_id = token_id.replace(' ', '').replace('-', '')
        token_password = token_password.replace(' ', '').replace('-', '')

        print(token_id, token_password)

        try:
            token = cls.objects.get(token_id=token_id, expires__gte=timezone.now())
        except cls.DoesNotExist:
            print("DID NOT FIND THE TOKEN!")
            return None

        if check_password(token_password, token.token_hash):
            return token

        return None

    @classmethod
    def use_token(cls, token_id, token_password):
        """Check the given token values and use the token if available. Returns the token if used."""
        token = cls.check_token(token_id, token_password)

        if token:
            token.user.email = token.email
            token.used = timezone.now()
            token.save()

        return token

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

