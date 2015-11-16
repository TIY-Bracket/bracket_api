# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 16, 13, 40, 40, 329158, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
