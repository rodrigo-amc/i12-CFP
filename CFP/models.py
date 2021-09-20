from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField
from django.core.validators import MinValueValidator
# Create your models here.

# region Utiles
class Localidad(models.Model):
    nombre = models.CharField(max_length=50)

class diaHora(models.Model):
    opcionDias = [
        ('L', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miercoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sabado'),
    ]
    dia = models.CharField(max_length=9, choices=opcionDias)
    hora = models.TimeField()
#endregion utiles


class CentroDeFormacion(models.Model):
    nombre = CharField(max_length=20)
    localidad = models.ForeignKey(Localidad, on_delete=DO_NOTHING)
    domicilio = models.CharField(max_length=150)
    email = models.EmailField()



class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    cenForm = models.ForeignKey(CentroDeFormacion, on_delete=DO_NOTHING)
    inscAbierta = models.BooleanField(default=False)
    habilitado = models.BooleanField(default=False)
    practico = models.BooleanField(default=True)
    cantHoras = models.PositiveIntegerField(validators=[MinValueValidator(4)])
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    diasHorarios = models.ManyToManyField(diaHora)