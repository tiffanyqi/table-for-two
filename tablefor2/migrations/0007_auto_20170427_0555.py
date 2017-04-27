# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0006_auto_20170427_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_authenticated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
        migrations.AddField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(default=datetime.datetime(2017, 4, 27, 5, 55, 1, 778105, tzinfo=utc), max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
