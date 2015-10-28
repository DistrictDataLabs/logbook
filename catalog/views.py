# catalog.views
# Views for the Catalog app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 16:27:57 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the Catalog app
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import messages
from braces.views import LoginRequiredMixin
from django.views.generic.edit import FormView
from catalog.forms import DatasetUploadForm

##########################################################################
## HTML/Web Views
##########################################################################

class DatasetUploadView(LoginRequiredMixin, FormView):

    template_name = "site/upload.html"
    form_class = DatasetUploadForm
    success_url = "/upload"

    def get_form_kwargs(self):
        """
        Add the request to the kwargs
        """
        kwargs = super(DatasetUploadView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Dataset added to the LogBook.')
        return super(DatasetUploadView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add ten most recent uploads to context
        """
        context = super(DatasetUploadView, self).get_context_data(**kwargs)
        return context
