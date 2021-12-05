# Generated by Django 3.2.3 on 2021-12-05 15:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFP', '0011_remove_curso_cantal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='centrodeformacion',
            old_name='domicilio',
            new_name='calle',
        ),
        migrations.AddField(
            model_name='centrodeformacion',
            name='altura',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='centrodeformacion',
            name='entre',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]