# Generated by Django 2.0 on 2017-12-24 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zaboj', '0010_auto_20171209_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deprecated_order_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
