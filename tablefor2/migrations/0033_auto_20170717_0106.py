# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0032_auto_20170710_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='distinct_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 1, 6, 56, 858493, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available_utc',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 1, 6, 56, 858512, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 1, 6, 56, 857178, tzinfo=utc)),
        ),
    ]
