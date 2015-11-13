# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151113_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(null=True, blank=True, max_length=128),
        ),
    ]
