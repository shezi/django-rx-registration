# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template

from .forms import RegistrationForm, LoginForm
from .utils import rxsettings

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
                subject_template = get_template('rx-registration/register_subject.djtxt')
                text_template = get_template('rx-registration/register_text.djtxt')

                ctx = Context({
                    'user': user,
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
                    # TODO: signal this to the user, probably?
                    pass
            
            return redirect(rxsettings.redirect_after_register)

    return render(request, 'rx-registration/register.djhtml', data)


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
