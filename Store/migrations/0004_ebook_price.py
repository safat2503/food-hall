# Generated by Django 4.2.3 on 2023-07-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_crisp_remove_ebook_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebook',
            name='price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
