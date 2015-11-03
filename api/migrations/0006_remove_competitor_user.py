# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151103_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitor',
            name='user',
        ),
    ]
