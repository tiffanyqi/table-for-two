# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0009_auto_20170501_0602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='ghangout',
            new_name='google_hangout',
        ),
    ]
