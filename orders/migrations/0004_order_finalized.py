# Generated by Django 2.0 on 2017-12-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20171225_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
    ]
