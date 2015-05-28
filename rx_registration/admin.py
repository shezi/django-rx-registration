from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import SignupConfirmationToken


class SignupTokenAdmin(admin.ModelAdmin):

    list_display = ('user', 'created', 'get_expired', 'expires', 'used', )

    list_filter = ('user', 'expires', 'used', )

    readonly_fields = ('created', 'token_id', 'token_hash', 'used')

    def get_expired(self, instance):
        return instance.expires < timezone.now()
    get_expired.boolean = True
    get_expired.short_description = _('is expired?')


admin.site.register(SignupConfirmationToken, SignupTokenAdmin)

