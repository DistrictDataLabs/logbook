# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.URLField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
