# catalog.forms
# Forms and other HTML data handling from the web front end.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Oct 28 15:47:44 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: forms.py [] benjamin@bengfort.com $

"""
Forms and other HTML data handling from the web front end.
"""

##########################################################################
## Imports
##########################################################################

from django import forms

##########################################################################
## Upload Form
##########################################################################

DATASET_ERROR_MSGS = {
    "required": "Please select an activity dataset to upload.",
    "invalid": "The activity dataset you provided is invalid, please select another.",
    "missing": "The activity dataset you specified is missing, please select another.",
    "empty": "The uploaded activity dataset is empty, cannot upload.",
    "max_length": "The activity dataset is too big, please submit a smaller CSV.",
}

class DatasetUploadForm(forms.Form):
    """
    Post an activity dataset and add the activity to the logbook.
    """

    dataset = forms.FileField(required=True, error_messages=DATASET_ERROR_MSGS)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DatasetUploadForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Save the dataset to S3
        """
        import time
        time.sleep(5)
