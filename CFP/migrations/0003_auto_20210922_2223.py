# Generated by Django 3.2.3 on 2021-09-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFP', '0002_auto_20210921_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diahora',
            name='dia',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='diahora',
            name='horaInicio',
            field=models.CharField(max_length=5),
        ),
    ]
