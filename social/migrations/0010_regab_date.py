# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_gab_gifid'),
    ]

    operations = [
        migrations.AddField(
            model_name='regab',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 14, 23, 59, 856498, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
