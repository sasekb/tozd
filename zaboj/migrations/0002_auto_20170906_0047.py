# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaboj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.FloatField(choices=[(0.5, '0,5 kg'), (1, '1 kg'), (2, '2 kg'), (3, '3 kg'), (4, '4 kg'), (5, '5 kg'), (6, '6 kg'), (7, '7 kg'), (8, '8 kg'), (9, '9 kg'), (10, '10 kg')]),
        ),
    ]
