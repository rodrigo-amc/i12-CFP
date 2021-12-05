# Generated by Django 3.2.3 on 2021-12-04 23:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0009_appuser_es_preceptor'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='dni',
            field=models.PositiveIntegerField(default=21000000, validators=[django.core.validators.MinValueValidator(20000000), django.core.validators.MaxValueValidator(99999999)]),
            preserve_default=False,
        ),
    ]