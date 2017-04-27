# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0004_auto_20170424_0415'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
