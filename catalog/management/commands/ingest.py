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
from django.contrib.auth.models import User
from catalog.models import Course, Enrollment, Instructor
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

    def get_user(self, email, full_name, counts):
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
            raise ValueError("No full name was supplied!")

        # Create the user since we couldn't find them
        counts['Inserted DDL Member Information'] += 1
        kwargs = {
            "email"      : email,
            "first_name" : " ".join(full_name[:-1]),
            "last_name"  : full_name[-1],
            "username"   : (full_name[0][0] + full_name[-1]).lower(),
        }

        return User.objects.create(**kwargs)

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
            "registeredforworkshop": self.handle_registration,
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
            try:
                row['User'] = self.get_user(row['Email'], row['FullName'], counts)
            except Exception as e:
                for notice in str(e).split("\n"):
                    notice = notice.strip()
                    if not notice: continue
                    counts["Couldn't create user: {}".format(notice)] += 1
                continue

            # Handle action according to jump table
            actions[action](row, counts)

        # Return the finialized counts
        return counts

    def handle_registration(self, row, counts):
        """
        Handle the student registration action.
        """

        # Find the course for the registration
        course = Course.objects.filter(name=row['Detail'])
        course = course.filter(begins__gte=row['ActionDate'])
        course = course.first()

        if not course:
            course = Course.objects.create(name=row['Detail'], begins=timezone.now())
        
        counts['Duplicate registrations'] += 1
        counts['New registrations'] += 2
