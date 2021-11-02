
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from Usuarios.forms import frmAlumno, frmUsuario
from .models import Alumno, appUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from CFP.models import Localidad

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


#region Alumno
def crearAlumno(request):
    ctxtGET = {
        'formAlumno': frmAlumno(),
        'formUser': frmUsuario,
        'titulo': 'Registrarse Como Alumno'
    }


    if request.method == 'POST':

        usrPost = frmUsuario(request.POST)

        #region "request.FILES"
        # OJO, para levantar los valores de los campos con archivos
        # Tengo que usar request.FILES ya que request.POST solo me
        # trae los valores de los inputs que no contienen archivos
        #endregion
        aluPost = frmAlumno(request.POST, request.FILES)

        if usrPost.is_valid() and aluPost.is_valid():
            #region Obtengo los valores de los formularios
            #appUser
            nombre = request.POST.get('first_name')
            apellido = request.POST.get('last_name')
            mail = request.POST.get('email')
            pswd = request.POST.get('password')

            #Alumno
            dni = request.POST.get('Dni')
            fNac = request.POST.get('fecha_nacimiento')
            
            # Acá uso "request.FILES" para obtener el
            # valor del input que contiene un archivo
            dni_img = request.FILES.get('DniImg')
            
            #region Cambio Nombre De La Imagen
            # Como nombre le pongo el dni
            nameImg = dni_img.name
            splittedN, splittedE = nameImg.split('.')
            splittedN = dni
            dni_img.name = splittedN+"."+splittedE
            #endregion

            autoriza = request.FILES.get('Autorizacion')
            tel = request.POST.get('Telefono')
            domc = request.POST.get('Domicilio')
            loc = request.POST.get('localidad')
            #endregion
            #print(type(dni_img))
            #Instancio "appUser"
            usuario = appUser(
                first_name = nombre,
                last_name = apellido,
                email = mail,
                password = pswd
            )

            usuario.set_password(pswd)
            usuario.username = mail
            usuario.es_alumno = True
            usuario.save()
            

            #Instancio Alumno
            alumno = Alumno(
                usr_alumno = usuario,
                Dni = dni,
                fecha_nacimiento = fNac,
                DniImg = dni_img,
                Autorizacion = autoriza,
                Telefono = tel,
                Domicilio = domc,
                localidad = Localidad.objects.get(pk=loc)
            )
            alumno.save()
            
            return redirect('login')

        else:
            for mensaje in usrPost.errors:
                messages.error(request, usrPost.errors[mensaje])
                return render(request, 'Usuarios/formAlumno.html',
                {
                    'formAlumno': aluPost,
                    'formUser': usrPost,
                    'titulo':'Registrarse Como Alumno'
                })

            for mensaje in aluPost.errors:
                messages.error(request, aluPost.errors[mensaje])
                return render(request, 'Usuarios/formAlumno.html',
                {
                    'formAlumno': aluPost,
                    'formUser': usrPost,
                    'titulo':'Registrarse Como Alumno'
                })

    else:
        return render(request, 'Usuarios/formAlumno.html', ctxtGET)
#endregion