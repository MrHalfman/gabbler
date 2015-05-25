# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0002_auto_20150525_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('by', models.ForeignKey(related_name='moderation_reports', to=settings.AUTH_USER_MODEL)),
                ('gab', models.ForeignKey(to='social.Gab')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
