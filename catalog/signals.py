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

from logbook.utils import htmlize
from catalog.models import Course

##########################################################################
## Course Signals
##########################################################################

@receiver(pre_save, sender=Course)
def course_render_details_markdown(sender, instance, *args, **kwargs):
    """
    Renders the details markdown on save.
    """
    if not instance.details:
        instance.details = None

    if instance.details is not None:
        instance.details_rendered = htmlize(instance.details)
    else:
        instance.details_rendered = None
