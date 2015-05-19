# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template

from . import get_stripe
from .forms import RegistrationForm, LoginForm
from locator.models import Location
from lazysignup.models import LazyUser
from lazysignup.utils import is_lazy_user

@transaction.atomic
def register(request):

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

            subject_template = get_template('rx-registration/register_subject.djtxt')
            text_template = get_template('rx-registration/register_text.djtxt')

            ctx = Context({
                'user': user,
            })

            subject = subject_template.render(ctx)
            text = text_template.render(ctx)
            FROM = '' # TODO: use a setting here

            send_mail(
                subject, text,
                FROM,
                [user.email], fail_silently=False)
            
            return redirect('TODO') # TODO: use a setting here!

    return render(request, 'rx-registration/register.djhtml', data)


def v_login(request):
    data = {}

    data['registration_form'] = RegistrationForm()
    data['form'] = LoginForm()

    if request.method == 'POST':
        data['form'] = form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('TODO')   # TODO: use a setting here!

    return render(request, 'rx-registration/login.djhtml', data)


def v_logout(request):
    messages.info(request, _('You have been logged out.'))
    logout(request)

    return redirect('TODO')  # TODO: use a setting here
