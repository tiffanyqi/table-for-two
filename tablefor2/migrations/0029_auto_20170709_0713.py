# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0028_auto_20170706_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='department',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='google_hangout',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='name_a_fun_fact_about_yourself',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='picture_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='timezone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='what_is_your_favorite_animal',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 9, 7, 13, 24, 481452, tzinfo=utc)),
        ),
    ]
