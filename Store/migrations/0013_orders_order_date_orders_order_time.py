# Generated by Django 4.2.3 on 2023-08-19 11:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0012_remove_merchantdiscount_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='order_time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
