# Generated by Django 3.2.3 on 2021-12-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0011_alter_profesor_dni'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumno',
            old_name='Domicilio',
            new_name='calle',
        ),
        migrations.AddField(
            model_name='alumno',
            name='altura',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumno',
            name='entre',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]