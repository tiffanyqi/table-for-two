# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0030_auto_20170710_0414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='time_available',
        ),
    ]
