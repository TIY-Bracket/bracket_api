# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151103_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('parent', models.CharField(max_length=255)),
                ('bracket', models.ForeignKey(to='api.Bracket')),
                ('competitor', models.ForeignKey(to='api.Competitor')),
            ],
        ),
        migrations.RemoveField(
            model_name='positions',
            name='bracket',
        ),
        migrations.RemoveField(
            model_name='positions',
            name='competitor',
        ),
        migrations.DeleteModel(
            name='Positions',
        ),
    ]
