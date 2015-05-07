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
    initial['plan'] = request.GET.get('plan')
    data['form'] = RegistrationForm(initial=initial)
    
    if request.method == 'POST':
        data['form'] = form = RegistrationForm(request.POST)
        if form.is_valid():

            if is_lazy_user(request.user):
                user = request.user
                LazyUser.objects.filter(user=user).delete()
                user.username=form.cleaned_data['username']
                user.email=form.cleaned_data['email']
            else:
                user = get_user_model()(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            ud = user.userdata

            ud.save()
            

            # Also ensure that stripe will start with the same setup-data as we are.
            from locator.stripe_utils import ensure_stripe_id
            ensure_stripe_id(user)

            subject_template = get_template('rx-registration/register_subject.djtxt')
            text_template = get_template('rx-registration/register_text.djtxt')

            ctx = Context({
                'user': user,
            })

            subject = subject_template.render(ctx)
            text = text_template.render(ctx)
            FROM = ''

            send_mail(
                subject, text,
                FROM,
                [user.email], fail_silently=False)
            
            return redirect('locator:locations')

    return render(request, 'rx-registration/register.djhtml', data)


def v_login(request):
    data = {}

    data['registration_form'] = RegistrationForm()
    data['form'] = LoginForm()

    if request.method == 'POST':
        data['form'] = form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('locator:locations')

    return render(request, 'rx-registration/login.djhtml', data)


def v_logout(request):
    messages.info(request, 'Sie haben sich von der Seite abgemeldet.')
    logout(request)

    return redirect('locator:main')
