# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalcontent',
            name='gif',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='additionalcontent',
            name='video',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
