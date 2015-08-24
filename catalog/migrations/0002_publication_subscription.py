# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import autoslug.fields
import markupfield.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, editable=False)),
                ('link', models.URLField(default=None, null=True, blank=True)),
                ('pubdate', models.DateField(default=None, null=True, blank=True)),
                ('pubtype', models.CharField(default=b'blog', max_length=12, choices=[(b'blog', b'blog'), (b'tutorial', b'tutorial'), (b'paper', b'paper'), (b'slides', b'slides'), (b'book', b'book')])),
                ('authors', models.ManyToManyField(related_name='publications', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'db_table': 'publications',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('details', markupfield.fields.MarkupField(default=None, help_text=b'Edit in Markdown', null=True, rendered_field=True, blank=True)),
                ('link', models.URLField(default=None, null=True, blank=True)),
                ('details_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('_details_rendered', models.TextField(null=True, editable=False)),
                ('subscribers', models.ManyToManyField(related_name='subscriptions', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
    ]
