# Generated by Django 4.2 on 2024-10-24 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_alter_venta_cod_venta_alter_ventaitems_codigo_venta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventaitems',
            name='codigo_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Venta', to='ventas.venta', verbose_name='Venta'),
        ),
    ]
