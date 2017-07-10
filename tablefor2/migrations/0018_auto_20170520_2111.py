# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0016_auto_20170505_0554'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='number_of_matches',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='timezone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time_available',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_entered_mixpanel',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(),
        ),
    ]
