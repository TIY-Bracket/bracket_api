# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_bracket_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bracket',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 15, 17, 30, 7, 504764, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
