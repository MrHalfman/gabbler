# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_moderationreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderationreport',
            name='reason',
            field=models.TextField(default='plop'),
            preserve_default=False,
        ),
    ]
