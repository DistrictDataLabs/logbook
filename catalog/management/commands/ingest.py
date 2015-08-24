# catalog.management.commands.ingest
# Ingest utility to grab data from a CSV file and insert into database.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Aug 23 21:18:54 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: ingest.py [] benjamin@bengfort.com $

"""
Ingest utility to grab data from a CSV file and insert into database.
"""

##########################################################################
## Imports
##########################################################################

import csv
import argparse

from dateutil import parser
from collections import Counter
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.models import User
from catalog.models import Course, Enrollment, Instructor
from catalog.models import Subscription, Publication
from members.models import Role, Membership
from django.core.management.base import BaseCommand, CommandError

##########################################################################
## Ingest Command
##########################################################################

EXPECTED_FIELDS = frozenset([
    'Email', 'FullName', 'Action', 'Detail', 'ActionDate', 'IPAddress'
])


def normalize(text):
    """
    Returns lowercased text with no spaces.
    """
    return text.lower().replace(" ", "")


class Command(BaseCommand):

    help = "Ingest data from a CSV file and insert into the database."

    def add_arguments(self, parser):
        """
        Add command line arguments to the argparse.ArgumentParser.
        """

        # Positional Arguments
        parser.add_argument(
            'data', metavar='PATH', nargs='+', type=argparse.FileType('r'),
            help='Activity CSV file with user to action detail'
        )

    def get_user(self, email, full_name, date, counts):
        """
        Get or creates a User object using the email address as the key.
        """
        # Perform various string handling
        email = normalize(email)
        full_name = full_name.strip().split()

        # Attempt to fetch the user from the database
        user = User.objects.filter(email=email).first()
        if user is not None:
            return user

        if not full_name:
            counts["Couldn't create user: No full name was supplied"] +=1
            return None

        # Create the user since we couldn't find them
        kwargs = {
            "email"      : email,
            "first_name" : " ".join(full_name[:-1]),
            "last_name"  : full_name[-1],
            "username"   : (full_name[0][0] + full_name[-1]).lower(),
            "date_joined": date,
        }

        try:
            user = User.objects.create(**kwargs)
            counts['Inserted DDL Member Information'] += 1
            return user
        except Exception as e:
            for notice in str(e).split("\n"):
                notice = notice.strip()
                if not notice: continue
                counts["Couldn't create user: {}".format(notice)] += 1
            return None

    def handle(self, **options):
        """
        Handle all command line input and write output to the console.
        """
        counts = Counter()
        for idx, data in enumerate(options['data']):
            counts += self.handle_ingest(data)

        for key, cnt in sorted(counts.items(), key=lambda k: k[0]):
            if key == 'rows': continue
            self.stdout.write("{}: {}".format(key, cnt))

        self.stdout.write("Read {} rows in {} data files.".format(counts['rows'], idx+1))

    def handle_ingest(self, data):
        """
        Handle an individual CSV file and associated errors and counts.
        """
        reader = csv.DictReader(data)
        counts = Counter()

        # Check for missing expected fields
        errors = EXPECTED_FIELDS - frozenset(reader.fieldnames)
        if errors:
            raise CommandError(
                "Missing required csv fields: {}".format(", ".join(errors))
            )

        # Jump table for handling different ingestion actions
        actions = {
            "registeredforworkshop": self.handle_enrollment,
            'taughtworkshop': self.handle_instructor,
            'taforworkshop': self.handle_instructor,
            'organizedworkshop': self.handle_instructor,
            'signedupfornewcoursenotifications': self.handle_subscription,
            'subscribedtoddlblog': self.handle_subscription,
            'wroteblogpost': self.handle_publication,
        }

        # Parse the activity csv file
        for row in reader:
            counts['rows'] += 1
            action = normalize(row['Action'])

            # Register any unhandled actions
            if action not in actions:
                counts["Skipped action {!r}: no handler implemented".format(row['Action'])] += 1
                continue

            # Convert the action date field to a datetime
            row['ActionDate'] = parser.parse(row['ActionDate'])

            # Try to add user to the row
            row['User'] = self.get_user(row['Email'], row['FullName'], row['ActionDate'], counts)
            if row['User'] is None: continue

            # Handle action according to jump table
            actions[action](row, counts)

        # Return the finialized counts
        return counts

    def handle_enrollment(self, row, counts):
        """
        Handle the student enrollment (registration) action.
        """
        # Assign the student membership to the user
        membership, created = Membership.objects.get_or_create(
            role=Role.objects.get(slug="student"), profile=row['User'].profile
        )
        if created:
            counts['New student role added'] += 1
        else:
            counts['Duplicate student role detected'] += 1

        # Find the course for the registration
        course = Course.objects.filter(name=row['Detail'])
        course = course.filter(begins__gte=row['ActionDate']).order_by('begins')
        course = course.first()

        if not course:
            counts['Course not found: {}'.format(row['Detail'])] += 1
            return

        kwargs = {
            'user': row['User'],
            'course': course,
            'result': Enrollment.GRADES.SC,
            'created': row['ActionDate'],
        }

        enroll, created = Enrollment.objects.get_or_create(**kwargs)
        if created:
            counts['New Enrollments'] += 1
        else:
            counts['Duplicate Enrollments'] += 1

    def handle_instructor(self, row, counts):
        """
        Handle the course and instructor creation action.
        """

        bdte = row['ActionDate'].date()
        dmin = datetime.combine(bdte, time.min)
        dmax = datetime.combine(bdte, time.max)

        # Find the course for the instructor
        course = Course.objects.filter(name=row['Detail'], begins__range=(dmin, dmax))
        course = course.first()

        if not course:
            course = Course.objects.create(
                name=row['Detail'],
                begins=datetime.combine(bdte, time(9,0)),
                finishes=datetime.combine(bdte, time(17,0)),
                course_type=Course.TYPES.workshop,
                created=row['ActionDate'],
            )

            print 'Created course: {}'.format(course)
            counts['Courses created from instructor records'] += 1

        # Find the role for the instructor
        role_slug = {
            "taughtworkshop":"instructor",
            "organizedworkshop":"organizer",
            "taforworkshop":"teaching-assistant",
        }[normalize(row['Action'])]
        role = Role.objects.get(slug=role_slug)

        # Create the instructor relationship to the course
        kwargs = {
            'role': role,
            'course': course,
            'user': row['User'],
            'created': row['ActionDate'],
        }

        instruct, created = Instructor.objects.get_or_create(**kwargs)
        if created:
            counts['New Instructor'] += 1
        else:
            counts['Duplicate Instructor'] += 1

        # Assign the instructor membership to the user
        membership, created = Membership.objects.get_or_create(
            role=role, profile=row['User'].profile
        )
        if created:
            counts['New {} role added'.format(role)] += 1
        else:
            counts['Duplicate {} role detected'.format(role)] += 1

    def handle_publication(self, row, counts):
        """
        Handles the publication action for authors. Right now this only works
        with blog posts and the authors that write those posts.
        """

        # Assign the author membership to the user
        membership, created = Membership.objects.get_or_create(
            role=Role.objects.get(slug="blog-author"), profile=row['User'].profile
        )
        if created:
            counts['New blog author role added'] += 1
        else:
            counts['Duplicate blog author role detected'] += 1

        # Attempt to fetch the publication from the name.
        pub, created = Publication.objects.get_or_create(
            title=row['Detail'], pubdate=row['ActionDate'].date()
        )

        if created:
            counts['New publication added'] += 1
            print "Created publication: {}".format(pub)
        else:
            counts['Duplicate publication detected'] += 1

        # Add the author relationship to the publication
        if pub.authors.filter(username=row['User'].username).exists():
            counts['Duplicate author not added to publication'] += 1
        else:
            pub.authors.add(row['User'])
            counts['Added author to publication'] += 1

    def handle_subscription(self, row, counts):
        """
        Handles the subscription action for email addresses.
        """

        # Assign the subscriber membership to the user
        membership, created = Membership.objects.get_or_create(
            role=Role.objects.get(slug="subscriber"), profile=row['User'].profile
        )
        if created:
            counts['New subscriber role added'] += 1
        else:
            counts['Duplicate subscriber role detected'] += 1

        # Find subscription in database
        slug = {
            'signedupfornewcoursenotifications': 'new-course-notifications',
            'subscribedtoddlblog': 'ddl-blog-syndication',
        }[normalize(row['Action'])]

        sub = Subscription.objects.get(slug=slug)

        # Add the subscriber relationship to the subscription
        if sub.subscribers.filter(username=row['User'].username).exists():
            counts['Duplicate subscriber not added to subscription'] += 1
        else:
            sub.subscribers.add(row['User'])
            counts['Added subscriber to {}'.format(sub)] += 1
