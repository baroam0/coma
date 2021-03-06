# Generated by Django 2.2 on 2021-01-14 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0001_initial'),
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiales.Material')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.Orden')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.Unidad')),
            ],
            options={
                'verbose_name_plural': 'Detalles Operaciones',
            },
        ),
    ]
