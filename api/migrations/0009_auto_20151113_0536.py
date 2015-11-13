# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20151112_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bracket',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='competitor',
            name='user',
        ),
        migrations.AddField(
            model_name='competitor',
            name='email',
            field=models.EmailField(blank=True, null=True, max_length=254),
        ),
    ]
