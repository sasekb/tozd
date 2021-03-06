# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 22:24
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distributer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('main', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, help_text='Ime kraja (brez poštne številke).', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='district',
            field=models.CharField(blank=True, help_text='Ime četrtne skupnosti (npr. "Bežigrad"). Lahko prazno.', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_union_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_nr',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Telefonska mora biti v formatu "+999999999".                                        Dovoljenih do 15 znakov.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='user',
            name='pickup_method',
            field=models.IntegerField(choices=[(1, 'Dostava na dom'), (2, 'Prevzem pri distributerju'), (3, 'Leteči')], help_text='1. Dostavmo na dom.                                                    2. Prevzem v svoji četrti/kraju.                                                    3. Prevzem na poti po dogovoru z distributerjem.', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, help_text='Ulica in hišna številka.', max_length=120, null=True),
        ),
    ]
