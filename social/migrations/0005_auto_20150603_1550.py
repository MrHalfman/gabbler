# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0004_moderationreport_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='GabOpinion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('likes', models.BooleanField(default=0)),
            ],
        ),
        migrations.AlterModelOptions(
            name='gab',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='gabopinion',
            name='gab',
            field=models.ForeignKey(related_name='opinions', to='social.Gab'),
        ),
        migrations.AddField(
            model_name='gabopinion',
            name='user',
            field=models.ForeignKey(related_name='opinions', to=settings.AUTH_USER_MODEL),
        ),
    ]
