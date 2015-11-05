# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151103_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='positions',
            old_name='bracket_id',
            new_name='bracket',
        ),
        migrations.RenameField(
            model_name='positions',
            old_name='competitor_id',
            new_name='competitor',
        ),
    ]
