# Generated by Django 3.2.3 on 2021-11-05 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0006_alter_alumno_dniimg'),
        ('CFP', '0006_remove_diahora_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Usuarios.profesor'),
        ),
    ]
