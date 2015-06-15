# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_mailnotifications_private_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 15, 12, 45, 13, 785806, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
