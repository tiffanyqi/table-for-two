# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0026_auto_20170706_0246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='toggle_power',
        ),
        migrations.AddField(
            model_name='profile',
            name='accept_matches',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 6, 3, 5, 49, 427074, tzinfo=utc)),
        ),
    ]
