# Generated by Django 4.0.6 on 2022-11-02 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'required': '입력하세요', 'unique': '이미 존재하는 ID 입니다.'}, max_length=254, unique=True),
        ),
    ]
