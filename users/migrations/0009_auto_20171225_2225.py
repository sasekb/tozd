# Generated by Django 2.0 on 2017-12-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20171224_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pickup_method',
            field=models.IntegerField(choices=[(1, 'Dostava na dom'), (2, 'Prevzem pri distributerju'), (3, 'Leteči')], help_text='1. Dostavmo na dom (+1€).                                                    2. Prevzem v svoji četrti/kraju.                                                    3. Prevzem na poti po dogovoru z distributerjem.', null=True),
        ),
    ]