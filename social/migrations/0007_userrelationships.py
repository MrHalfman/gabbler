# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0006_auto_20150603_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRelationships',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('following', models.ForeignKey(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
