# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0010_auto_20170504_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='extra_saved_information',
            field=models.BooleanField(default=False),
        ),
    ]
