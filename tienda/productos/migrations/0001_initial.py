# Generated by Django 4.2 on 2024-10-22 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('precio', models.FloatField(max_length=10)),
                ('existencia', models.IntegerField(max_length=10)),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='categoria', to='productos.categoria', verbose_name='categoria')),
            ],
        ),
    ]
