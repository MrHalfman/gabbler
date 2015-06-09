# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_auto_20150606_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='gab',
            name='gifId',
            field=models.CharField(default=None, max_length=64, null=True, blank=True),
        ),
    ]
