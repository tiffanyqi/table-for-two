# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0035_auto_20170808_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
