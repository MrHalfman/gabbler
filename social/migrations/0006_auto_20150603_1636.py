# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20150603_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gabopinion',
            old_name='likes',
            new_name='like',
        ),
    ]
