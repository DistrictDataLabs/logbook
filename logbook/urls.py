# logbook.urls
# Application url definition and routers.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 13:21:31 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Application url definition and routers.
"""

##########################################################################
## Imports
##########################################################################

from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin

from logbook.views import HomePageView

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    # Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Application URLs
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    # Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
