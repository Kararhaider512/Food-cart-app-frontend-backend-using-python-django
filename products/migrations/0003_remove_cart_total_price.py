# Generated by Django 5.1.3 on 2024-12-04 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
    ]
