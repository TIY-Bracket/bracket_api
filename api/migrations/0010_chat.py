# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151113_0536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('text', models.CharField(max_length=255)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
    ]
