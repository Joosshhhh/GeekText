# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0004_auto_20170527_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authorize_net_profile_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
