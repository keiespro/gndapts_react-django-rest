# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 07:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160909_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='contact_information',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]