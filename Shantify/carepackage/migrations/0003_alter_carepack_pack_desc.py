# Generated by Django 4.0.4 on 2022-05-03 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carepackage', '0002_carepack_prepared_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carepack',
            name='pack_desc',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Pack Description'),
        ),
    ]
