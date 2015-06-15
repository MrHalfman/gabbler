# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_update',
        ),
    ]
