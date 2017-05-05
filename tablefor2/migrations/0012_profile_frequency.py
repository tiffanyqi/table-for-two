# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0011_profile_extra_saved_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='frequency',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
