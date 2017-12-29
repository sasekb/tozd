# Generated by Django 2.0 on 2017-12-21 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_packagetype'),
        ('products', '0007_product_package_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='package_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.PackageType'),
        ),
    ]
