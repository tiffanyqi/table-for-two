# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0024_auto_20170702_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 2, 22, 25, 47, 92050, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
