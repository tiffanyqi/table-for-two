# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0020_auto_20170520_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_entered_mixpanel',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 21, 4, 23, 56, 386394, tzinfo=utc)),
        ),
    ]
