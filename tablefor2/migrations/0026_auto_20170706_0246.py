# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0025_auto_20170702_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='toggle_power',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 6, 2, 46, 55, 66178, tzinfo=utc)),
        ),
    ]
