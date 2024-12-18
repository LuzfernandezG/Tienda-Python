# Generated by Django 4.2 on 2024-11-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_productos_descripcion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos'),
        ),
    ]
