from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField
from django.core.validators import MinValueValidator
# Create your models here.

# region Utiles
class Localidad(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class diaHora(models.Model):
    dia = models.CharField(max_length=9)
    horaInicio = models.CharField(max_length=6)
    horaFin = models.CharField(max_length=6)
    def __str__(self):
        return self.dia
#endregion utiles


class CentroDeFormacion(models.Model):
    nombre = CharField(max_length=20)
    localidad = models.ForeignKey(Localidad, on_delete=DO_NOTHING)
    domicilio = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


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

    def __str__(self):
        return self.nombre