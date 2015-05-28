# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, mail_admins
from django.db import transaction
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template

from .forms import RegistrationForm, LoginForm
from .utils import rxsettings
from .models import SignupConfirmationToken

import logging


@transaction.atomic
def register(request):
    """Register a new user."""
    data = {}

    initial = {}
    data['form'] = RegistrationForm(initial=initial)
    
    if request.method == 'POST':
        data['form'] = form = RegistrationForm(request.POST)
        if form.is_valid():

            user = get_user_model()(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            if rxsettings.confirm_registration:
                password, token = SignupConfirmationToken.make_token(user=user, email=user.email)
                user.email = 'none@example.com'  # if you MUST have one...
                user.save()

                subject_template = get_template('rx-registration/register_subject.djtxt')
                text_template = get_template('rx-registration/register_text.djtxt')

                ctx = Context({
                    'user': user,
                    'token': token,
                    'password': password,
                })

                subject = subject_template.render(ctx)
                text = text_template.render(ctx)
                email_from = rxsettings.confirm_registration_from

                try:
                    send_mail(
                        subject, text,
                        email_from,
                        [user.email], fail_silently=False)
                except IOError:
                    messages.warning(request, get_template('rx-registration/signup_confirmation_mail_failed.djtxt').render(request=request))

                    error_data = {
                        'subject': subject, 'text': text, 'user': user,
                        'email': user.email,
                    }

                    mail_admins(
                        subject='Signup email could not be sent',
                        message='Signup confirmation message could not be sent\nError data is: {}'.format(error_data),
                        fail_silently=True,
                    )

                    logging.error('Signup email could not be sent: {}'.format(error_data))

            return redirect(rxsettings.redirect_after_register)

    return render(request, 'rx-registration/register.djhtml', data)


def register_confirm(request, token_id, token_password):
    """Confirm a registration token and set a user's email address to confirmed."""

    token = SignupConfirmationToken.use_token(token_id, token_password)
    if token:
        token.user.backend = 'rx-registration'
        login(request, token.user)

        messages.info(request, get_template('rx-registration/registration_confirmed.djtxt').render(request=request))

        return redirect(rxsettings.redirect_after_login)

    return render(request, 'rx-registration/signup_confirm_failed.djhtml')


def v_login(request):
    data = {}

    data['registration_form'] = RegistrationForm()
    data['form'] = LoginForm()

    if request.method == 'POST':
        data['form'] = form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(rxsettings.redirect_after_login)

    return render(request, 'rx-registration/login.djhtml', data)


def v_logout(request):
    messages.info(request, _('You have been logged out.'))
    logout(request)

    return redirect(rxsettings.redirect_after_logout)
