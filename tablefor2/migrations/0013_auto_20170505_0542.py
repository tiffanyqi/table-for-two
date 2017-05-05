# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0012_profile_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='google_hangout',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
