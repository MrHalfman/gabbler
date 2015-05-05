# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150310_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='city',
        ),
        migrations.RemoveField(
            model_name='place',
            name='country',
        ),
        migrations.AddField(
            model_name='place',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
