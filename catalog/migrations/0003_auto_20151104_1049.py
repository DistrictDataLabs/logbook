# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_publication_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ('-pubdate', '-created'), 'get_latest_by': 'pubdate'},
        ),
    ]
