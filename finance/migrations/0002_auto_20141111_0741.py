# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='ticker',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
