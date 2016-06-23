# members.models
# Models that store information about faculty and students.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:24:48 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [a700ca8] benjamin@bengfort.com $

"""
Models that store information about faculty and students.
"""

##########################################################################
## Imports
##########################################################################


from django.db import models
from model_utils import Choices
from django.conf import settings
from logbook.utils import nullable
from autoslug import AutoSlugField
from urllib.parse import urlencode
from model_utils.models import TimeStampedModel
from markupfield.fields import MarkupField
from django.core.urlresolvers import reverse

##########################################################################
## DDL Roles and Membership Information
##########################################################################

class Role(TimeStampedModel):
    """
    Roles define the relationship of DDL members to DDL activities. E.g.
    faculty, student, instructor, TA, etc. Roles are stored in the Database
    so that they can be updated on demand.

    Roles can be stored in a hierarchical fashion. E.g. instructor can be a
    subrole of faculty by using the parent/subrole organization.
    """

    name     = models.CharField(max_length=64, unique=True)
    slug     = AutoSlugField(populate_from='name', unique=True)
    details  = MarkupField(markup_type='markdown', help_text='Edit in Markdown', **nullable)
    parent   = models.ForeignKey('self', related_name='subroles', **nullable)

    class Meta:
        db_table = 'roles'
        get_latest_by = 'created'

    def __str__(self):
        return self.name


class Membership(TimeStampedModel):
    """
    Membership defines the various roles that a DDL user has, and when they
    acheived that role and if that role is still active. Some roles require
    sponsorship, so this field also saves sponsor information.
    """

    role        = models.ForeignKey('members.Role')
    profile     = models.ForeignKey('members.Profile')
    active      = models.BooleanField(default=True)
    deactivated = models.DateTimeField(**nullable)
    sponsor     = models.ForeignKey('auth.User', related_name='sponsorship', **nullable)

    class Meta:
        db_table = 'membership'
        get_latest_by = 'created'

    def __str__(self):
        return "{} role of {}".format(self.role, self.profile)

##########################################################################
## User Profile Model for DDL Members
##########################################################################

class Profile(TimeStampedModel):
    """
    Stores extra information about a user or DDL member.
    """

    user         = models.OneToOneField('auth.User', editable=False)
    email_hash   = models.CharField(max_length=32, editable=False)
    organization = models.CharField(max_length=255, **nullable)
    location     = models.CharField(max_length=255, **nullable)
    biography    = MarkupField(markup_type='markdown', help_text='Edit in Markdown', **nullable)
    twitter      = models.CharField(max_length=100, **nullable)
    linkedin     = models.URLField(**nullable)
    roles        = models.ManyToManyField('members.Role', through='members.Membership', related_name='members')

    class Meta:
        db_table = 'member_profiles'

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = u"{} <{}>".format(self.full_name, self.user.email)
        return email.strip()

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=settings.GRAVATAR_ICON_SIZE)

    @property
    def gravatar_badge(self):
        return self.get_gravatar_url(size=64)

    def get_gravatar_url(self, size=None, default=None):
        """
        Comptues the gravatar url from an email address
        """
        size    = size or settings.GRAVATAR_DEFAULT_SIZE
        default = default or settings.GRAVATAR_DEFAULT_IMAGE
        params  = urlencode({'d': default, 's': str(size)})

        return "http://www.gravatar.com/avatar/{}?{}".format(
            self.email_hash, params
        )

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:user-detail', args=(self.user.pk,))

    def get_absolute_url(self):
        """
        Returns the detail view url for the object
        """
        return reverse('member-detail', args=(self.user.username,))

    def __str__(self):
        return self.full_email
