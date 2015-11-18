# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_competitor_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 17, 17, 36, 34, 478087, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
