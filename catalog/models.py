# catalog.models
# Models that define how we describe DDL events in the database.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 16:27:03 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models that define how we describe DDL events in the database.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from autoslug import AutoSlugField
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from logbook.utils import nullable, humanizedelta
from django.core.urlresolvers import reverse

##########################################################################
## Event Base Class
##########################################################################

class DDLEvent(TimeStampedModel):
    """
    Defines fields that all DDL events share no matter their event type.
    """

    name     = models.CharField(max_length=255)
    slug     = AutoSlugField(populate_from='name', unique=True)
    begins   = models.DateTimeField(**nullable)
    finishes = models.DateTimeField(**nullable)
    details  =  MarkupField(markup_type='markdown', help_text='Edit in Markdown', **nullable)

    class Meta:
        abstract = True

    def duration(self, humanize=False):
        """
        Returns the duration of the event, either in seconds or as a humanized
        time stamp (e.g. the number of days, hours, etc.).
        """
        seconds = (self.finishes - self.begins).total_seconds()
        if humanize:
            return humanizedelta(seconds=seconds)
        return seconds

    def get_absolute_url(self):
        """
        Return the detail view of the event object.
        """
        raise NotImplementedError("DDL Events shoud have a page view!")

    def __unicode__(self):
        return self.name


##########################################################################
## Courses
##########################################################################

class Course(DDLEvent):
    """
    Almost everything DDL offers is a course, from a Webinar to a Workshop.
    This database field will track courses and their instructors as well as
    other important information about the course.

    Note that longer events like Incubators and Research Labs are not this.
    """

    TYPES  = Choices('workshop', 'webinar', 'lecture')

    course_type = models.CharField(max_length=10, choices=TYPES, default=TYPES.workshop)
    instructors = models.ManyToManyField('auth.User', through='catalog.Instructor', related_name='courses')

    class Meta:
        db_table = 'courses'
        ordering = ('-begins', '-created')
        get_latest_by   = 'created'
        unique_together = ('name', 'begins')

    def get_absolute_url(self):
        """
        Return the detail view of the Course object
        """
        return reverse('course', kwargs={'slug': self.slug})

##########################################################################
## Instructors
##########################################################################

class Instructor(TimeStampedModel):
    """
    A relationship between a user and a course that describes how they
    instructed the course. Note this is similar to the members.Membership
    relationship, but between courses and users, not profiles and roles.
    """

    course = models.ForeignKey('catalog.Course')
    user   = models.ForeignKey('auth.User')
    role   = models.ForeignKey('members.Role', related_name='+')
