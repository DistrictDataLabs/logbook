# logbook.settings.production
# The Django settings for LogBook in Production
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:22:02 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: production.py [6e3ca6b] benjamin@bengfort.com $

"""
The Django settings for LogBook in Production
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False

## Hosts
ALLOWED_HOSTS    = ['ddl-logbook.herokuapp.com', 'logbook.districtdatalabs.com']

## Static files served by WhiteNoise
STATIC_ROOT = 'staticfiles'
