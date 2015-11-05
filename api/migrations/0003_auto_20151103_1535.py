# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_competitor_positions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitor',
            old_name='user_id',
            new_name='user',
        ),
    ]
