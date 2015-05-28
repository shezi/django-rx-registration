from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

    # user urls
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.v_login, name='login'),
    url(r'^logout/$', views.v_logout, name='logout'),

    url(
        r'^register/confirm/(?P<token_id>[a-zA-Z0-9 -]{8,128})/(?P<token_password>[a-zA-Z0-9 -]{8,128})/',
        views.register_confirm,
        name='register-confirm'
    ),

    url(r'^password/$', 'django.contrib.auth.views.password_change',
        {'post_change_redirect': ''}, # TODO: use a setting here?
        name='password'),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': 'rx-registration:password_reset_done'},
        name="password_reset"
        ),
    url(r'^password/reset/sent/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done',
        ),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': 'rx-registration:password_reset_complete'},
        name='password_reset_confirm',
        ),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete',
        ),


)
