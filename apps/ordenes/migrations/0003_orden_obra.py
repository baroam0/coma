# Generated by Django 2.2 on 2021-01-15 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0001_initial'),
        ('ordenes', '0002_detalleorden'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='obra',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obras.Obra'),
        ),
    ]
