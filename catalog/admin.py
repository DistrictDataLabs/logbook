# catalog.admin
# Admin models for ORM management of the catalog models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 16:26:30 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin models for ORM management of the catalog models.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from catalog.models import Course, Instructor, Enrollment

##########################################################################
## Inline Adminstration
##########################################################################


class InstructorInline(admin.TabularInline):
    """
    Inline administration descriptor for course instructors
    """

    model = Instructor
    extra = 1
    verbose_name_plural = 'instructors'


class EnrollmentInline(admin.TabularInline):
    """
    Inline administration descriptor for course enrollment
    """

    model = Enrollment
    extra = 5
    verbose_name_plural = 'enrollment'


class CourseAdmin(admin.ModelAdmin):
    """
    Define new Course admin view
    """

    inlines = (InstructorInline, EnrollmentInline)


##########################################################################
## Register Admin
##########################################################################

admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment)
