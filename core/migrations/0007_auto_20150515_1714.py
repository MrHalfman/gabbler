# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150509_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='place',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='place',
            name='zoom',
        ),
        migrations.AddField(
            model_name='place',
            name='country',
            field=models.TextField(max_length=150, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(default=b"I'm true member of Gabbler and it's already not bad!", max_length=300, blank=True),
            preserve_default=True,
        ),
    ]
