# Generated by Django 3.2 on 2021-05-16 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='results', to='jobs.search'),
        ),
    ]