# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-28 00:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0036_auto_20171120_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAvailability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matched_group_users', models.TextField(null=True)),
                ('time_available', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_available_utc', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='match_type',
            field=models.CharField(default=b'one-on-one', max_length=20),
        ),
        migrations.AddField(
            model_name='groupavailability',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
