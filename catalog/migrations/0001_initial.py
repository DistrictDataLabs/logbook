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
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('begins', models.DateTimeField(default=None, null=True, blank=True)),
                ('finishes', models.DateTimeField(default=None, null=True, blank=True)),
                ('details', markupfield.fields.MarkupField(default=None, help_text=b'Edit in Markdown', null=True, rendered_field=True, blank=True)),
                ('course_type', models.CharField(default=b'workshop', max_length=10, choices=[(b'workshop', b'workshop'), (b'webinar', b'webinar'), (b'lecture', b'lecture')])),
                ('details_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')])),
                ('_details_rendered', models.TextField(null=True, editable=False)),
            ],
            options={
                'ordering': ('-begins', '-created'),
                'db_table': 'courses',
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('result', models.CharField(default=None, max_length=2, null=True, blank=True, choices=[(b'SC', b'Satisfactory Completion'), (b'I', b'Incomplete'), (b'RE', b'Registered, but Never Attended'), (b'AT', b'Attendance Verfied'), (b'W', b'Withdrawn')])),
                ('course', models.ForeignKey(to='catalog.Course')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'enrollment',
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('course', models.ForeignKey(to='catalog.Course')),
                ('role', models.ForeignKey(related_name='+', to='members.Role')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'instructors',
                'get_latest_by': 'created',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(related_name='taught_courses', through='catalog.Instructor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='enrolled_courses', through='catalog.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='instructor',
            unique_together=set([('user', 'course', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('name', 'begins')]),
        ),
    ]
