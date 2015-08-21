# logbook.views
# Default application views for the system.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 13:20:11 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Default application views for the system.
"""

##########################################################################
## Imports
##########################################################################

from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView

##########################################################################
## Views
##########################################################################

class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = "site/home.html"
