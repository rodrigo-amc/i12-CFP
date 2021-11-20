from django.db import models
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
    practico = models.BooleanField(default=False)
    cantHoras = models.PositiveIntegerField(validators=[MinValueValidator(4)])
    cupoMin = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    cupoMax = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    diasHorarios = models.ManyToManyField(diaHora)
    cantAl = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    #region Evitar Error De Referencia Circular
    # https://stackoverflow.com/questions/28868610/django-importerror-cannot-import-model#28869260
    # No me deja importar el modelo "Profesor" de la app "Usuarios" porque me devuelve
    # un error relacionado con referencia circular, aunque no hay ninguna referencia
    # circular...
    # La solucion (stackoverflow) es definir el parámetro que corresponde al modelo en la relacion
    # como un string con la forma "App.Modelo" y de ese modo se evita el import que genera
    # el error.
    # endregion 
    profesor = models.ForeignKey('Usuarios.Profesor', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


