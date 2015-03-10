# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150310_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='place',
            field=models.ForeignKey(default=None, blank=True, to='core.Place', null=True),
            preserve_default=True,
        ),
    ]
