from django.db import models
from django.contrib.auth.models import AbstractUser
#from Carreras.models import Carrera
from django.core.validators import MaxValueValidator, MinValueValidator

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
    usr_alumno = models.OneToOneField(appUser, on_delete=models.CASCADE, primary_key=True)
    
    dni = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(20000000), MaxValueValidator(99999999)])
    #nombre = es el campo "first_name" de AbstractUser
    #apellido = es el campo "last_name" de AbstractUser
    

    """ opcion_sexo = [
        ('f', 'Femenino'),
        ('m', 'Masculino')
    ]
    sexo = models.CharField(max_length=9, choices=opcion_sexo)

    opcion_casadao = [
        ('c', 'casado'),
        ('s', 'soltero')
    ]
    est_civil = models.CharField(max_length=7, choices=opcion_casadao)
    hijos = models.PositiveIntegerField(default=0, blank=True, null=True) """
    fecha_nacimiento = models.DateField()

    telefono = models.CharField(max_length=20)
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único
    domicilio = models.CharField(max_length=100)

    #Esto deberia relacionar a tablas pero por ahora lo dejo asi
    localidad = models.CharField(max_length=100)
    partido = models.CharField(max_length=100)

    #ForeingKey es una relacion de 1 a N
    #En este caso 1 Carrera Tiene N Alumnos. 1 Alumno tiene solo 1 Carrera 
#    carrera = models.ForeignKey(Carrera, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.usr_alumno.username





class Profesor(models.Model):
    usr_profesor = models.OneToOneField(appUser, on_delete=models.CASCADE, primary_key=True)

    #nombre = es el campo "first_name" de AbstractUser
    #apellido = es el campo "last_name" de AbstractUser
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único

    def __str__(self):
        return self.usr_profesor.username
