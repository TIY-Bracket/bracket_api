# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bracket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('start_dt', models.DateTimeField(blank=True, null=True)),
                ('end_dt', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
