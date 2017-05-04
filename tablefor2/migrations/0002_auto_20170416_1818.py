# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablefor2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='matched_user',
        ),
        migrations.RenameField(
            model_name='availability',
            old_name='user',
            new_name='profile',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='matched_user',
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
