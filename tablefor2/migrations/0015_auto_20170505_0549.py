# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0014_auto_20170505_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_entered_mixpanel',
            field=models.DateField(),
        ),
    ]
