# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0019_auto_20170520_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='time_available_utc',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 20, 21, 44, 47, 617335, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 20, 21, 44, 23, 585462, tzinfo=utc)),
        ),
    ]
