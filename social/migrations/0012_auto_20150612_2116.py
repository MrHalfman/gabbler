# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_auto_20150610_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gab',
            old_name='gifId',
            new_name='gif_id',
        ),
        migrations.RemoveField(
            model_name='gab',
            name='extras',
        ),
        migrations.AddField(
            model_name='gab',
            name='picture',
            field=models.URLField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='gab',
            name='video',
            field=models.URLField(default=None, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='AdditionalContent',
        ),
    ]
