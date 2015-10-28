# catalog.templatetags.catalog
# Tags specific to the catalog library including Bootstrap helpers.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Oct 28 13:00:46 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: catalog.py [] benjamin@bengfort.com $

"""
Tags specific to the catalog library including Bootstrap helpers.
"""

##########################################################################
## Imports
##########################################################################

from django import template
from django.core.urlresolvers import resolve, Resolver404

##########################################################################
## Module Constants
##########################################################################

## Classes
EMPTY    = ""
ACTIVE   = "active"

## Register Decorator
register = template.Library()

##########################################################################
## Tags
##########################################################################

@register.simple_tag
def active_page(request, name):
    """
    Returns active if the request is resolved to the name.
    """
    if not request:
        return EMPTY

    try:
        url_name = resolve(request.path_info).url_name

        # Break off any "-" spaces in the name for model views
        if "-" in url_name:
            url_name = url_name.split("-")[0]

        return ACTIVE if url_name == name else EMPTY
    except Resolver404:
        return EMPTY
