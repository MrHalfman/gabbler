# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_userrelationships'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelationships',
            name='following',
            field=models.ForeignKey(related_name='rel_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userrelationships',
            name='user',
            field=models.ForeignKey(related_name='rel_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
