# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-19 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_building_amenities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='contact_information',
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_email',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_facebook',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_relation_property',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='contact_whatsapp',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
