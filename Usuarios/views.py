
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from Usuarios.forms import frmAlumno, frmPreceptor, frmUsuario, frmProfesor, frmUsrProf, Preceptor
from .models import Alumno, Profesor, appUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from CFP.models import CentroDeFormacion, Curso, Localidad

# Create your views here.

@login_required
def logIn(request):
    if request.user.is_authenticated:
        return redirect('/menu')
    else:
        return redirect('accounts/login')


@login_required
def menu(request):
    
    if request.user.is_superuser:
        adminCtxt={
            'titulo':'Menu De Administracion'
        }
        return render(request, 'Usuarios/menuAdmin.html', adminCtxt)
    
    elif request.user.es_preceptor:
        user = appUser.objects.get(pk=request.user.id)
        precCtxt={
            'usuario':user,
            'titulo':'Preceptor'
        }
        
        return render(request, 'Usuarios/menuPreceptor.html', precCtxt)
        
    else:
        return redirect('/')



#region CRUD Alumno
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



#region CRUD Profesores
@login_required
def lstProfesores(request):
    if request.user.is_superuser:
        profesores = appUser.objects.all().filter(es_profesor=True)
        ctx={
            'profesores': profesores,
            'titulo': 'Profesores'
        }
        return render(request, 'Usuarios/profesores.html', ctx)
    else:
        return redirect('login')



@login_required
def crearProfesor(request):
    if request.user.is_superuser:
        getDict={
            'titulo': 'Registrar Nuevo Profesor',
            'frmUsuario': frmUsrProf(),
            'formProfesor': frmProfesor()
        }
        if request.method == 'POST':
            frmPostU = frmUsrProf(request.POST)
            frmPostP = frmProfesor(request.POST)
            if frmPostP.is_valid() and frmPostU.is_valid():
                nombre = request.POST.get('first_name')
                apellido = request.POST.get('last_name')
                mail = request.POST.get('email')
                pswd = str(nombre).lower()+str(apellido).lower()
                tel = request.POST.get('telefono')

                usuario = appUser(
                    first_name = nombre,
                    last_name = apellido,
                    email = mail,
                    password = pswd
                )
                usuario.set_password(pswd)
                usuario.username = mail
                usuario.es_profesor = True
                usuario.save()

                profe = Profesor(
                    usr_profesor = usuario,
                    telefono = tel

                )
                profe.save()

                """ return HttpResponse(
                    'nombre: {0}</br>Apellido: {1}</br>Email: {2}</br>Password: {3}</br>Telefono: {4}'
                    .format(nombre, apellido, mail, pswd, tel)
                    ) """
                return redirect('profesores')

            else:
                for mensaje in frmPostU.errors:
                    messages.error(request, frmPostU.errors[mensaje])
                    return render(request, 'Usuarios/formProfesor.html',
                    {
                        'formProfesor': frmPostP,
                        'frmUsuario': frmPostU,
                        'titulo':'Registrar Nuevo Profesor'
                    })

                for mensaje in frmPostP.errors:
                    messages.error(request, frmPostP.errors[mensaje])
                    return render(request, 'Usuarios/formProfesor.html',
                    {
                        'formProfesor': frmPostP,
                        'frmUsuario': frmPostU,
                        'titulo':'Registrar Nuevo Profesor'
                    })
        
        else:
            return render(request, 'Usuarios/formProfesor.html', getDict)
        
    else:
        return redirect('home')



@login_required
def editarProfesor(request, idUsr):
    if request.user.is_superuser:
        usr = appUser.objects.get(pk=idUsr)
        profe = Profesor.objects.get(pk=idUsr)

        if request.method == 'GET':
            frmUsr = frmUsrProf(instance=usr)
            frmPro = frmProfesor(instance=profe)

            ctxGet = {
                'titulo': 'Editar Datos De Profesor',
                'frmUsuario': frmUsr,
                'formProfesor': frmPro
            }

            return render(request, 'Usuarios/formProfesor.html', ctxGet)
        
        elif request.method == 'POST':
            usrPost = frmUsrProf(request.POST, instance=usr)
            proPost = frmProfesor(request.POST, instance=profe)

            if usrPost.is_valid() and proPost.is_valid:
                usrPost.save()
                proPost.save()
                return redirect('profesores')
            else:
                for mensaje in usrPost.errors:
                    messages.error(request, usrPost.errors[mensaje])
                    return render(request, 'Usuarios/formProfesor.html',
                    {
                        'formProfesor': proPost,
                        'frmUsuario': usrPost,
                        'titulo':'Editar Datos De Profesor'
                    })

                for mensaje in proPost.errors:
                    messages.error(request, proPost.errors[mensaje])
                    return render(request, 'Usuarios/formProfesor.html',
                    {
                        'formProfesor': proPost,
                        'frmUsuario': usrPost,
                        'titulo':'Editar Datos De Profesor'
                    })
        
        else:
            return HttpResponse('naditas')    
    else:
        return HttpResponse('banana')



@login_required
def profDeshabilitar(request, idUsr):
    usr = appUser.objects.get(pk = idUsr)
    if request.user.is_superuser and usr.es_profesor:
        usr.is_active = False
        usr.save()
        return redirect('profesores')
    else:
        return HttpResponse('naditas')
#endregion



#region CRUD Preceptores
@login_required
def lstPreceptores(request):
    if request.user.is_superuser:
        preceptores = appUser.objects.all().filter(es_preceptor=True)
        ctx={
            'usrsPrec': preceptores,
            'titulo': 'Preceptores'
        }
        return render(request, 'Usuarios/preceptores.html', ctx)
    else:
        return redirect('login')



@login_required
def crearPreceptor(request):
    if request.user.is_superuser:
        getDict={
            'titulo': 'Registrar Nuevo Preceptor',
            # Uso el mismo formulario que usi para
            # "Profesor" ya que me sirve para este
            # modelo
            'frmUsuario': frmUsrProf(),
            'formPreceptor': frmPreceptor()
        }
        if request.method == 'POST':
            frmPostUsr = frmUsrProf(request.POST)
            frmPostPre = frmPreceptor(request.POST)

            if frmPostPre.is_valid() and frmPostUsr.is_valid():
                nombre = request.POST.get('first_name')
                apellido = request.POST.get('last_name')
                mail = request.POST.get('email')
                pswd = str(nombre).lower()+str(apellido).lower()
                tel = request.POST.get('telefono')
                centro = CentroDeFormacion.objects.get(pk=request.POST.get('cfp'))

                usuario = appUser(
                    first_name = nombre,
                    last_name = apellido,
                    email = mail,
                    password = pswd
                )
                print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#')
                print(pswd)
                print(usuario.password)
                print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#')
                usuario.set_password(pswd)
                usuario.username = mail
                usuario.es_preceptor = True
                usuario.save()

                preceptor = Preceptor(
                    usr = usuario,
                    telefono = tel,
                    cfp = centro 
                )
                preceptor.save()

                return redirect('preceptores')

            else:
                for mensaje in frmPostUsr.errors:
                    messages.error(request, frmPostUsr.errors[mensaje])
                    return render(request, 'Usuarios/formPreceptor.html',
                    {
                        'formPreceptor': frmPostPre,
                        'frmUsuario': frmPostUsr,
                        'titulo':'Registrar Nuevo Preceptor'
                    })

                for mensaje in frmPostPre.errors:
                    messages.error(request, frmPostPre.errors[mensaje])
                    return render(request, 'Usuarios/formPreceptor.html',
                    {
                        'formPreceptor': frmPostPre,
                        'frmUsuario': frmPostUsr,
                        'titulo':'Registrar Nuevo Preceptor'
                    })
        
        else:
            return render(request, 'Usuarios/formPreceptor.html', getDict)
        
    else:
        return redirect('home')



@login_required
def editarPreceptor(request, idUsr):
    if request.user.is_superuser:
        usr = appUser.objects.get(pk=idUsr)
        prec = Preceptor.objects.get(pk=idUsr)

        if request.method == 'GET':
            frmUsr = frmUsrProf(instance=usr)
            frmPre = frmPreceptor(instance=prec)

            ctxGet = {
                'titulo': 'Editar Datos De Preceptor',
                'frmUsuario': frmUsr,
                'formPreceptor': frmPre
            }

            return render(request, 'Usuarios/formPreceptor.html', ctxGet)
        
        elif request.method == 'POST':
            usrPost = frmUsrProf(request.POST, instance=usr)
            prePost = frmPreceptor(request.POST, instance=prec)

            if usrPost.is_valid() and prePost.is_valid:
                usrPost.save()
                prePost.save()
                return redirect('preceptores')
            else:
                for mensaje in usrPost.errors:
                    messages.error(request, usrPost.errors[mensaje])
                    return render(request, 'Usuarios/formPreceptor.html',
                    {
                        'formPreceptor': prePost,
                        'frmUsuario': usrPost,
                        'titulo':'Editar Datos De Preceptor'
                    })

                for mensaje in prePost.errors:
                    messages.error(request, prePost.errors[mensaje])
                    return render(request, 'Usuarios/formPreceptor.html',
                    {
                        'formPreceptor': prePost,
                        'frmUsuario': usrPost,
                        'titulo':'Editar Datos De Preceptor'
                    })
        
        else:
            return HttpResponse('naditas')    
    else:
        return redirect('home')



@login_required
def deshabilitarPreceptor(request, idUsr):
    usr = appUser.objects.get(pk = idUsr)
    if request.user.is_superuser and usr.es_preceptor:
        usr.is_active = False
        usr.save()
        return redirect('preceptores')
    else:
        return redirect('home')
#endregion Preceptores
