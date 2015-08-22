# members.admin
# Administrative interface for members in Logbook.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:24:11 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Administrative interface for members in Logbook.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from members.models import Profile

##########################################################################
## Inline Adminstration
##########################################################################


class ProfileInline(admin.StackedInline):
    """
    Inline administration descriptor for profile object
    """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    """
    Define new User admin
    """

    inlines = (ProfileInline, )

##########################################################################
## Register Admin
##########################################################################

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
