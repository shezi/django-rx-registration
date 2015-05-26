# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):

    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=60,
        label=_("User name"),
        error_messages={
            'invalid': _("In the user name, only numbers, alphabetical characters and the characters  ., +, -, _ and @"
                         " may appear.")},
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Password"),
    )

    def clean(self):
        """Verify that the user can be logged in (and store it in self)."""
        user = authenticate(**self.cleaned_data)
        if user is not None and user.is_active:
            self.user = user
            return self.cleaned_data
        raise forms.ValidationError(_("Your log in data could not be found. Please check your input and try again."))


class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=60,
                                label=_("User name"),
                                error_messages={
                                    'invalid': _("In the user name, only numbers, alphabetical characters and the "
                                                 "characters  ., +, -, _ and @ may appear.")})
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (repeated for checking)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("This username is already taken."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """Make sure the email isn't taken yet."""
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("This email address is already in use. Please enter a different email "
                                          "address!"))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields are different. Please enter the same password "
                                              "in both fields."))
        return self.cleaned_data
