# members.signals
# Signals management for the Members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 10:43:03 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [a700ca8] benjamin@bengfort.com $

"""
Signals management for the Members app.
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from members.models import Profile, Membership
from django.contrib.auth.models import User

##########################################################################
## User Signals
##########################################################################

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    digest = hashlib.md5(instance.email.lower().encode('utf-8')).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()

##########################################################################
## Membership Signals
##########################################################################

@receiver(pre_save, sender=Membership)
def deactivate_membership(sender, instance, *args, **kwargs):
    """
    Saves the deactivated timestamp if the membership becomes non-active
    """

    if not instance.active:
        if not instance.deactivated:
            instance.deactivated = timezone.now()
