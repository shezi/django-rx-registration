# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):

    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=60,
        label="Benutzername",
        error_messages={'invalid': "Im Benutzernamen dürfen nur Zahlen, Buchstaben und die Zeichen ., +, -, _ und @ vorkommen."}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Passwort"
    )

    def clean(self):
        """Verify that the user can be logged in (and store it in self)."""
        user = authenticate(**self.cleaned_data)
        if user is not None and user.is_active:
            self.user = user
            return self.cleaned_data
        raise forms.ValidationError("Die Anmeldedaten können nicht gefunden werden. Bitte überprüfen Sie die Daten und versuchen Sie es erneut.")


class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=60,
                                label="Benutzername",
                                error_messages={'invalid': "Im Benutzernamen dürfen nur Zahlen, Buchstaben und die Zeichen ., +, -, _ und @ vorkommen."})
    email = forms.EmailField(label="E-Mail")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Passwort")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Passwort (erneut, zur Kontrolle)")

    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             initial=False,
                             label=mark_safe('Ich habe die <a href="/agb/">allgemeinen Geschäftsbedingungen</a> gelesen und stimme ihnen zu.'),
                             error_messages={'required': "Sie müssen den AGB zustimmen, um sich registrieren zu können."})
    tos.left = True

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("Dieser Benutzername ist bereits vergeben.")
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """Make sure the email isn't taken yet."""
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError("Diese Emailadresse wird bereits für einen Benutzer genutzt. Bitte geben Sie eine andere Emailadresse an!")
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
                raise forms.ValidationError("Die beiden Passwort-Felder stimmen nicht überein.")
        return self.cleaned_data
