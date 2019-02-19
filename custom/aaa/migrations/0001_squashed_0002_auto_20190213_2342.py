# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-13 23:44
# flake8: noqa
from __future__ import absolute_import
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('end_time', models.DateTimeField(help_text='Time the aggregation completed', null=True)),
                ('domain', models.TextField()),
                ('step', models.TextField(help_text='Slug for the step of the aggregation')),
                ('aggregation_window_start', models.DateTimeField()),
                ('aggregation_window_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CcsRecord',
            fields=[
                ('domain', models.TextField()),
                ('state_id', models.TextField(null=True)),
                ('district_id', models.TextField(null=True)),
                ('block_id', models.TextField(null=True)),
                ('supervisor_id', models.TextField(null=True)),
                ('awc_id', models.TextField(null=True)),
                ('taluka_id', models.TextField(null=True)),
                ('phc_id', models.TextField(null=True)),
                ('sc_id', models.TextField(null=True)),
                ('village_id', models.TextField(null=True)),
                ('person_case_id', models.TextField()),
                ('ccs_record_case_id', models.TextField(primary_key=True, serialize=False)),
                ('opened_on', models.DateField()),
                ('closed_on', models.DateField(null=True)),
                ('hrp', models.TextField(help_text='High Risk Pregnancy', null=True)),
                ('child_birth_location', models.TextField(null=True)),
                ('edd', models.DateField(null=True)),
                ('add', models.DateField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('domain', models.TextField()),
                ('state_id', models.TextField(null=True)),
                ('district_id', models.TextField(null=True)),
                ('block_id', models.TextField(null=True)),
                ('supervisor_id', models.TextField(null=True)),
                ('awc_id', models.TextField(null=True)),
                ('taluka_id', models.TextField(null=True)),
                ('phc_id', models.TextField(null=True)),
                ('sc_id', models.TextField(null=True)),
                ('village_id', models.TextField(null=True)),
                ('household_case_id', models.TextField(null=True)),
                ('person_case_id', models.TextField(unique=True)),
                ('child_health_case_id', models.TextField(primary_key=True, serialize=False)),
                ('opened_on', models.DateField(help_text='child_health.opened_on')),
                ('closed_on', models.DateField(help_text='child_health.opened_on', null=True)),
                ('dob', models.DateField(null=True)),
                ('sex', models.TextField(null=True)),
                ('migration_status', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Woman',
            fields=[
                ('domain', models.TextField()),
                ('state_id', models.TextField(null=True)),
                ('district_id', models.TextField(null=True)),
                ('block_id', models.TextField(null=True)),
                ('supervisor_id', models.TextField(null=True)),
                ('awc_id', models.TextField(null=True)),
                ('taluka_id', models.TextField(null=True)),
                ('phc_id', models.TextField(null=True)),
                ('sc_id', models.TextField(null=True)),
                ('village_id', models.TextField(null=True)),
                ('household_case_id', models.TextField(null=True)),
                ('person_case_id', models.TextField(primary_key=True, serialize=False)),
                ('opened_on', models.DateField()),
                ('closed_on', models.DateField(null=True)),
                ('pregnant_ranges', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ranges.DateRangeField(), help_text='The ranges in which a ccs_record has been opened and the baby has not been born', null=True, size=None)),
                ('dob', models.DateField(null=True)),
                ('marital_status', models.TextField(null=True)),
                ('sex', models.TextField(null=True)),
                ('migration_status', models.TextField(null=True)),
                ('fp_current_method_ranges', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ranges.DateRangeField(), help_text="Ranges of time when eligible_couple.fp_current_method != 'none'", null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WomanHistory',
            fields=[
                ('person_case_id', models.TextField(primary_key=True, serialize=False)),
                ('fp_current_method_history', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=2), null=True, size=None)),
                ('fp_preferred_method_history', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=2), null=True, size=None)),
            ],
        ),
    ]