# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0022_auto_20170619_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name_a_fun_fact_about_yourself',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='what_is_your_favorite_animal',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 2, 22, 19, 11, 293900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='recurringavailability',
            name='time',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
