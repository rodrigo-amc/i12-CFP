from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import DO_NOTHING
from CFP.models import Localidad, Curso
# Create your models here.
"""
Por ahora solo voy a crear Alumno y Profesor
Para el usuario Administrador uso el usuario
que implementa el framework
"""

class appUser(AbstractUser):
    es_alumno = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)

    def __str__(self):
        return self.username



class Alumno(models.Model):
    #nombre = es el campo "first_name" de AbstractUser
    #apellido = es el campo "last_name" de AbstractUser
    usr_alumno = models.OneToOneField(appUser, on_delete=models.CASCADE, primary_key=True)

    Dni = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(20000000), MaxValueValidator(99999999)])
    
    fecha_nacimiento = models.DateField()

    DniImg = models.ImageField()
    Autorizacion = models.ImageField()

    Telefono = models.CharField(max_length=20)
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único
    Domicilio = models.CharField(max_length=100)

    localidad = models.ForeignKey(Localidad, on_delete=DO_NOTHING)

    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.usr_alumno.username



class Profesor(models.Model):
    usr_profesor = models.OneToOneField(appUser, on_delete=models.CASCADE, primary_key=True)
    telefono = models.CharField(max_length=20)
    #nombre = es el campo "first_name" de AbstractUser
    #apellido = es el campo "last_name" de AbstractUser
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único

    def __str__(self):
        return self.usr_profesor.username
