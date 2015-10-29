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

import argparse

from collections import Counter
from catalog.parser import ActivityParser
from django.core.management.base import BaseCommand, CommandError

##########################################################################
## Ingest Command
##########################################################################

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

    def handle(self, **options):
        """
        Handle all command line input and write output to the console.
        """
        counts = Counter()
        parser = ActivityParser()

        for idx, data in enumerate(options['data']):
            try:
                counts += parser.parse(data)
            except Exception as e:
                raise CommandError(str(e))


        for key, cnt in sorted(counts.items(), key=lambda k: k[0]):
            if key == 'rows': continue
            self.stdout.write("{}: {}".format(key, cnt))


        self.stdout.write("Read {} rows in {} data files.".format(counts['rows'], idx+1))
