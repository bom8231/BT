# Generated by Django 4.0.6 on 2022-08-30 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0003_remove_buy_lat_remove_buy_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='buy',
            name='long',
            field=models.FloatField(default=0),
        ),
    ]