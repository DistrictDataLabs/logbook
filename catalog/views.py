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

import time

from operator import itemgetter
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
        print "FORM VALID"
        start   = time.time()
        counts  = form.save()

        message = (
            'Read {:,d} rows in the uploaded dataset in {:0.3f} seconds.'
            .format(counts.pop('rows'), time.time() - start)
        )

        messages.success(self.request, message)
        self.request.session['report'] = sorted(counts.items(), key=itemgetter(0))
        return super(DatasetUploadView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add ten most recent uploads to context
        """
        context = super(DatasetUploadView, self).get_context_data(**kwargs)
        context['report'] = self.request.session.pop("report", [])

        return context
