# Generated by Django 4.0.6 on 2022-09-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0004_buy_lat_buy_long'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]