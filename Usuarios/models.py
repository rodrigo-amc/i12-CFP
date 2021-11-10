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

    # "upload_to" especifica la subcarpeta dentro de "zMedia" en donde se van a subir las imagenes
    DniImg = models.ImageField(upload_to='alumnos')
    Autorizacion = models.ImageField(blank=True, null=True, upload_to='alumnos/')

    Telefono = models.CharField(max_length=20)
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único
    Domicilio = models.CharField(max_length=100)

    localidad = models.ForeignKey(Localidad, on_delete=DO_NOTHING)

    curso = models.ManyToManyField(Curso, through='CursoAlumno')

    def __str__(self):
        return self.usr_alumno.username



# Este modelo deberia estar en la aplicacion CFP, pero lo pongo acá
# porque sino el framework me devuelve error E331
class CursoAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=DO_NOTHING)
    curso = models.ForeignKey(Curso, on_delete=DO_NOTHING)
    #porcAsist = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    porcAsist = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notaCurso = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(10)])
    aprobado = models.BooleanField(default=False)




class Profesor(models.Model):
    usr_profesor = models.OneToOneField(appUser, on_delete=models.CASCADE, primary_key=True)
    telefono = models.CharField(max_length=20)
    #nombre = es el campo "first_name" de AbstractUser
    #apellido = es el campo "last_name" de AbstractUser
    #email= es el campo "email" de AbstractUser
    #OJO edité "AbstractUser" (/django/contrib/auth/models.py) para que el campo email sea único

    def __str__(self):
        name = self.usr_profesor.first_name
        lname = self.usr_profesor.last_name
        fname = str(name+' '+lname)
        return fname
