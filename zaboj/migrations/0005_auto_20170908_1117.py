# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zaboj', '0004_auto_20170906_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='like',
        ),
        migrations.RemoveField(
            model_name='vegetable',
            name='user',
        ),
    ]
