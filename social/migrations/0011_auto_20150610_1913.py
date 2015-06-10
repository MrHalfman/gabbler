# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_regab_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='gab',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='user2',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='additionalcontent',
            name='gif',
        ),
        migrations.RemoveField(
            model_name='gab',
            name='reply',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='FriendShip',
        ),
        migrations.DeleteModel(
            name='PrivateMessage',
        ),
    ]
