# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import markupfield.fields
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('active', models.BooleanField(default=True)),
                ('deactivated', models.DateTimeField(default=None, null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('email_hash', models.CharField(max_length=32, editable=False)),
                ('organization', models.CharField(default=None, max_length=255, null=True, blank=True)),
                ('location', models.CharField(default=None, max_length=255, null=True, blank=True)),
                ('biography', markupfield.fields.MarkupField(default=None, help_text=b'Edit in Markdown', null=True, rendered_field=True, blank=True)),
                ('biography_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('_biography_rendered', models.TextField(null=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('details', markupfield.fields.MarkupField(default=None, help_text=b'Edit in Markdown', null=True, rendered_field=True, blank=True)),
                ('details_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('_details_rendered', models.TextField(null=True, editable=False)),
                ('parent', models.ForeignKey(related_name='subroles', default=None, blank=True, to='members.Role', null=True)),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(related_name='members', through='members.Membership', to='members.Role'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(to='members.Profile'),
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.ForeignKey(to='members.Role'),
        ),
        migrations.AddField(
            model_name='membership',
            name='sponsor',
            field=models.ForeignKey(related_name='sponsorship', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
