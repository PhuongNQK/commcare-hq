# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 18:03
from __future__ import unicode_literals

import corehq.apps.reports.models
from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportssidebarordering',
            name='config',
            field=jsonfield.fields.JSONField(default=list, help_text=b'An array of arrays. Each array represents a heading in the sidebar navigation. The first item in each array is a string, which will be the title of the heading. The second item in the array is another array, each item of which is the name of a report class. Each of these reports will be listed under the given heading in the sidebar nav.', validators=[corehq.apps.reports.models.ordering_config_validator]),
        ),
    ]
