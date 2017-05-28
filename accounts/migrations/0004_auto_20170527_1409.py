# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 18:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_user_authorize_net_profile_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userdefaultaddress',
            name='billing',
        ),
        migrations.RemoveField(
            model_name='userdefaultaddress',
            name='shipping',
        ),
        migrations.RemoveField(
            model_name='userdefaultaddress',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserAddress',
        ),
        migrations.DeleteModel(
            name='UserDefaultAddress',
        ),
    ]
