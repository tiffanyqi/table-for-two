# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0008_auto_20170427_0555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='division',
            new_name='department',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_authenticated',
        ),
        migrations.AddField(
            model_name='profile',
            name='date_entered_mixpanel',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='preferred_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
