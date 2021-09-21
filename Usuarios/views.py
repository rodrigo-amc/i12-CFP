from django.contrib.auth import login

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Alumno, appUser
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def logIn(request):
    if request.user.is_authenticated:
        return redirect('/menu')
    else:
        return redirect('accounts/login')


@login_required
def menu(request):
    """ contexto ={
        'usuario' : appUser.is_superuser
    } """
    if request.user.is_superuser:
        adminCtxt={
            'titulo':'Menu Administracion'
        }
        return render(request, 'Usuarios/menuAdmin.html', adminCtxt)
    
    elif request.user.es_alumno:
        alumno = Alumno.objects.get(pk=request.user.id)
        #carrera = Carrera.objects.get(id=alumno.carrera_id)
        #resolucion = carrera.resolucion
        aluCtxt={
            'titulo' : 'Menu Alumno',
         #   'carrera':carrera,
         #   'resolucion': resolucion,
        }
        return render(request, 'Usuarios/menuAlumno.html', aluCtxt)
    
    elif request.user.es_profesor:
        proCtxt={
            'titulo':'Menu Profesor'
        }
        return render(request, 'Usuarios/menuProfesor.html', proCtxt)
    else:
        return HttpResponse('No tiene permiso para acceder')