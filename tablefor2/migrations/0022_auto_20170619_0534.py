# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0021_auto_20170521_0423'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringAvailability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=50, null=True)),
                ('time', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 19, 5, 34, 36, 479163, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='recurringavailability',
            name='profile',
            field=models.ForeignKey(to='tablefor2.Profile'),
        ),
    ]
