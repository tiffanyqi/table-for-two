# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_available', django_unixdatetimefield.fields.UnixDateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('division', models.CharField(max_length=50, null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('ghangout', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='matched_user',
            field=models.ManyToManyField(to='tablefor2.Profile', through='tablefor2.Availability'),
        ),
        migrations.AddField(
            model_name='availability',
            name='matched_user',
            field=models.ForeignKey(to='tablefor2.Match'),
        ),
        migrations.AddField(
            model_name='availability',
            name='user',
            field=models.ForeignKey(to='tablefor2.Profile'),
        ),
    ]
