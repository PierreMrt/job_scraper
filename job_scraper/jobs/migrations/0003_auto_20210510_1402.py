# Generated by Django 3.2 on 2021-05-10 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20210509_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='search_key',
        ),
        migrations.AlterField(
            model_name='search',
            name='country',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='search',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]
