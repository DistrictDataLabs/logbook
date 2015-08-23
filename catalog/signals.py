# catalog.signals
# Signals for handling model events in the catalog app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 17:06:20 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for handling model events in the catalog app.
"""

##########################################################################
## Imports
##########################################################################

from django.dispatch import receiver
from django.db.models.signals import pre_save

from catalog.models import Course

##########################################################################
## Course Signals
##########################################################################
