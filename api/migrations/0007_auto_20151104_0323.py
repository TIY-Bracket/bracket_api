# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_competitor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='competitor',
            field=models.ForeignKey(blank=True, to='api.Competitor', null=True),
        ),
    ]
