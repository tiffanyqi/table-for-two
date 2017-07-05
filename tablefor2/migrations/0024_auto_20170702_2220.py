# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0023_auto_20170702_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture_url',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 2, 22, 20, 47, 833147, tzinfo=utc)),
        ),
    ]
