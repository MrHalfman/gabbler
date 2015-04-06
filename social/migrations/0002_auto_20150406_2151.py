# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gab',
            name='reply',
            field=models.ForeignKey(related_name='replies', blank=True, to='social.Gab', null=True),
            preserve_default=True,
        ),
    ]
