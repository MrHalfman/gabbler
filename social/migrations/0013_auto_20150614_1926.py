# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_auto_20150612_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationreport',
            name='gab',
            field=models.ForeignKey(related_name='reports', to='social.Gab'),
        ),
    ]
