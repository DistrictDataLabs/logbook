# catalog.apps
# Describes the Catalog application for Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 17:25:26 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Describes the Catalog application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Catalog Config
##########################################################################

class CatalogConfig(AppConfig):

    name = 'catalog'
    verbose_name = 'Catalog'

    def ready(self):
        import catalog.signals
