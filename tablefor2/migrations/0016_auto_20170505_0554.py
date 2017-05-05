# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0015_auto_20170505_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_entered_mixpanel',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
