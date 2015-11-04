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

import requests

from django import forms
from bs4 import BeautifulSoup
from urlparse import urlparse
from datetime import datetime
from django.conf import settings
from autoslug.settings import slugify
from catalog.parser import slugify as username_slugify
from django.contrib.auth.models import User

from catalog.models import Publication
from catalog.parser import ActivityParser
from members.models import Membership, Role

##########################################################################
## Module Constants
##########################################################################

PUBDATE_FORMAT = "%B %d, %Y"

DATASET_ERROR_MSGS = {
    "required": "Please select an activity dataset to upload.",
    "invalid": "The activity dataset you provided is invalid, please select another.",
    "missing": "The activity dataset you specified is missing, please select another.",
    "empty": "The uploaded activity dataset is empty, cannot upload.",
    "max_length": "The activity dataset is too big, please submit a smaller CSV.",
}

##########################################################################
## Upload Form
##########################################################################


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
        Parse the dataset
        """
        parser  = ActivityParser()
        dataset = self.cleaned_data['dataset']

        # Execute the parsing
        dataset.open('rb')
        counts  = parser.parse(dataset)
        dataset.close()

        return counts


class LinkFetchForm(forms.Form):
    """
    Submit a URL to lookup the publication.
    """

    link   = forms.URLField(required=True)


    def clean_link(self):
        """
        Validate a link such that its domain is in the list of valid
        publication domains and that we haven't already added the link to the
        database (because then there is nothing we can do).
        """

        data = self.cleaned_data['link']
        urlp = urlparse(data)

        # Test to ensure is in the valid domains
        if urlp.netloc not in settings.PUBLICATION_DOMAINS:
            raise forms.ValidationError(
                "Domain {!r} is not a valid publication domain. "
                "Only DDL publications can be fetched."
                .format(urlp.netloc,)
            )

        # If the link is in the DB - don't do any work.
        if Publication.objects.filter(link=data).exists():
            raise forms.ValidationError(
                "This link has already been added to the database!"
            )

        return data

    def get_author(self, name):
        """
        Attempts to retrieve an author by the full name from the database.
        """
        parts = name.split()
        uname = parts[0][0] + parts[-1] if len(parts) > 1 else parts[0]
        uname = username_slugify(uname)
        return User.objects.get(username=uname)

    def fetch(self):
        """
        Fetches the blog post, parses it and returns a dictionary of relevant
        values and information. Use this method sparingly.
        """
        link = self.cleaned_data['link']
        resp = requests.get(link)
        soup = BeautifulSoup(resp.content, "html5lib")

        return {
            "title": soup.find(class_='kaia_header_title').text.strip(),
            "authors": soup.find(class_="name_link").text.strip().split(" and "),
            "pubdate": datetime.strptime(soup.find(class_="entry_date").text.strip(), PUBDATE_FORMAT).date(),
            "link": link,
        }

    def save(self):
        """
        Parses and saves the publication to the database.
        """
        kwargs   = self.fetch()

        # Fetch authors first to error early if we can't find the user.s
        authors  = [
            self.get_author(name) for name in kwargs.pop('authors', [])
        ]

        # Get publication by slug or create it with the discovered attributes
        pub, crt = Publication.objects.update_or_create(slug=slugify(kwargs['title']), defaults=kwargs)

        # Add authors to the publication if any
        for author in authors:
            # Make sure the author has the correct role
            _ = Membership.objects.get_or_create(
                role=Role.objects.get(slug="blog-author"), profile=author.profile
            )

            # Add author to the publication
            if author not in pub.authors.all():
                pub.authors.add(author)

        return pub, crt
