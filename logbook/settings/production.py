# logbook.settings.production
# The Django settings for LogBook in Production
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:22:02 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: production.py [] bbengfort@districtdatalabs.com $

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
ALLOWED_HOSTS    = ['logbook.districtdatalabs.com']

## Static files served by Nginx
STATIC_ROOT = '/var/www/logbook/static'
MEDIA_ROOT  = '/var/www/logbook/media'
