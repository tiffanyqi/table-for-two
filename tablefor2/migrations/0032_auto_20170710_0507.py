# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0031_remove_availability_time_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='time_available',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 5, 7, 16, 930281, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available_utc',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 5, 7, 16, 930309, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 5, 7, 16, 928393, tzinfo=utc)),
        ),
    ]
