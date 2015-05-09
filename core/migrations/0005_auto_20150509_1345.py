# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150505_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='city',
            field=models.TextField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='zoom',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
