# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0033_auto_20170717_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='preferred_name',
            new_name='preferred_first_name',
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 6, 1, 55, 56, 466307, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available_utc',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 6, 1, 55, 56, 466329, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 6, 1, 55, 56, 464925, tzinfo=utc)),
        ),
    ]
