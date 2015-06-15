# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_user_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlink',
            name='type',
        ),
        migrations.RemoveField(
            model_name='userlink',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserLink',
        ),
        migrations.DeleteModel(
            name='UserLinkTypes',
        ),
    ]
