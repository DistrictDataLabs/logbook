#!/usr/bin/env python
# manage.py
# Django default management commands, with some special sauce.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jun 01 21:05:38 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: manage.py [] bbengfort@windsorview.com $

"""
Django default management commands, with some special sauce.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import dotenv

##########################################################################
## Main Method
##########################################################################

if __name__ == "__main__":
    ## Manage Django Environment
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logbook.settings.production")

    ## Execute Django utility
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
