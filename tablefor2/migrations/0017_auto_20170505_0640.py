# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0016_auto_20170505_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='time_available',
            field=models.DateTimeField(),
        ),
    ]
