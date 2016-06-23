# catalog.tests
# Testing library for the Catalog app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 16:27:35 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tests.py [7072b57] benjamin@bengfort.com $

"""
Testing library for the Catalog app.
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase
from catalog.parser import ActivityParser
from catalog.parser import normalize, slugify

##########################################################################
## Parsing Test Cases
##########################################################################


class ParsingTests(TestCase):

    def test_slugify(self):
        """
        Check that the slugify function works appropriately.
        """

        cases = (
            u'bob sled',
            u'B!ob "@Sled.?!',
            u'bob-sled',
            u'BOB-SLED',
            u'bob                sled',
            u"b'ob sled.",
        )

        for case in cases:
            self.assertEqual(slugify(case), u'bob-sled')

    def test_normalize(self):
        """
        Check that the normalize function works correctly.
        """

        cases = (
            u'bob sled',
            u'bobsled',
            u'BOB  SLED',
            u'bob                sled',
            u'BOB   sled',
        )

        for case in cases:
            self.assertEqual(normalize(case), u'bobsled')
