from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from CFP.forms import frmCentroFormacion, frmCursos, frmLocalidad
from django.contrib import messages

from Usuarios.models import Alumno, CursoAlumno, Profesor, appUser
from .models import CentroDeFormacion, Curso, Localidad
from django.db.models import Q
# Create your views here.


def home(request):
    
    # Recibo el usuario logeuado
    usr = request.user

    def getIfAlumno():
        '''Si el usuarui logueado es alumno
        devuelve el objeto de alumno que
        uso en el template para comprobar
        si el alumno está asociado con
        el curso'''
        alufn = ''
        if usr.is_authenticated and usr.es_alumno:
            alufn = Alumno.objects.get(pk = usr.id)
        return alufn

    amno = getIfAlumno()

    #region Localidades/Cursos
    #Todos Los Cursos
    cursosAll = Curso.objects.all()

    #Valor del campo de busqueda 
    busqueda = request.POST.get('localidad')
    
    #Todas las localidades de los cursos existentes
    locs = []

    #Guardo cada localidad asociada al CFP de cada Curso
    #Solo una vez
    for curso in cursosAll:
        
        localidad = curso.cenForm.localidad
        
        # Este es el "filtro" de busqueda. Si "busqueda" tiene un valor, hace la comparacion.
        if busqueda and ( (busqueda in str(localidad)) or (busqueda in str(localidad).lower()) ):
            # Si 
            locs.append(localidad)
            break
        elif not busqueda:
        # Si no hay valor de busqueda completa la lista con todas
        # las localidades

            # Si la localidad existe en la lista saltea la iteracion
            if localidad in locs:
                continue
            else:
                locs.append(localidad)
    
    #print("########################################")
    #print(locs)
    #endregion Localidades

    ctxtHome = {
        'cursos' : cursosAll,
        'localidades':locs,
        'usuario' : usr,
        'alumno' : amno
    }
    return render(request, 'CFP/home.html', ctxtHome)



#region Localidades
@login_required
def localidadNueva(request):
    if request.user.is_superuser:
        
        formLoc = frmLocalidad()
        ctxt = {
            'form': formLoc,
            'titulo': 'Nueva Localidad'
        }

        if request.method == 'POST':
            formPost = frmLocalidad(request.POST)

            if formPost.is_valid():
                formPost.save()
                return redirect('/localidades')
            else:
                for mensaje in formPost.errors:
                    messages.error(request, formPost.errors[mensaje])
                    return render(request, 'CFP/localidadForm.html', {'form': formPost, 'titulo': 'Nueva Localidad'})
        
        else:
            return render(request, 'CFP/localidadForm.html', ctxt)

    else:
        return HttpResponse('Solo disponible para usuario Administrador')



@login_required
def localidades(request):
    ctxt = {
        'lstLocalidades' : Localidad.objects.all()
        }

    return render(request, 'CFP/localidades.html', ctxt)



@login_required
def localidadEditar(request, idLocalidad):
    locEditar = Localidad.objects.get(pk=idLocalidad)
    frEditar = frmLocalidad()

    if request.method == 'GET':
        frEditar = frmLocalidad(instance=locEditar)
        ctxGET = {
            'form':frEditar,
            'titulo':'Editar Localidad'
        }
        return render(request, 'CFP/localidadForm.html', ctxGET)
    
    else:
        frEditar = frmLocalidad(request.POST, instance=locEditar)
        
        if frEditar.is_valid():
            frEditar.save()
        else:
            ctxtPOST = {
                'form': frEditar,
                'titulo': 'Editar Localidad - Corregir Errores'
            }
            for mensaje in frEditar.errors:
                messages.error(request, frEditar.errors[mensaje])
                return render(request, 'CFP/localidadForm.html', ctxtPOST)
        
        return redirect('/localidades')



def localidadBorrar(request, idLocalidad):
    locBorrar = Localidad.objects.get(pk=idLocalidad)
    locBorrar.delete()
    return redirect('/localidades')
#endregion Localidades



#region Centros De Formacion
@login_required
def centros(request):
    ctxt = {
        'centros' : CentroDeFormacion.objects.all(),
        'titulo':'Centros De Formacion'
    }
    return render(request, 'CFP/centros.html', ctxt)



@login_required
def centroNuevo(request):
    if request.user.is_superuser:
        
        formulario = frmCentroFormacion()
        ctxt = {
            'form': formulario,
            'titulo': 'Nuev Centro De Formacion'
        }

        if request.method == 'POST':
            formPost = frmCentroFormacion(request.POST)

            if formPost.is_valid():
                formPost.save()
                return redirect('/centros')
            else:
                for mensaje in formPost.errors:
                    messages.error(request, formPost.errors[mensaje])
                    return render(request, 'CFP/centrosForm.html', {'form': formPost, 'titulo': 'Nuevo Dentro De Formacion'})
        
        else:
            return render(request, 'CFP/centrosForm.html', ctxt)

    else:
        return HttpResponse('Solo disponible para usuario Administrador')



@login_required
def centroEditar(request, idCentro):
    cenEditar = CentroDeFormacion.objects.get(pk=idCentro)
    frEditar = frmCentroFormacion()

    if request.method == 'GET':
        frEditar = frmCentroFormacion(instance=cenEditar)
        ctxGET = {
            'form':frEditar,
            'titulo':'Editar Centro De Formacion'
        }
        return render(request, 'CFP/centrosForm.html', ctxGET)
    
    else:
        frEditar = frmCentroFormacion(request.POST, instance=cenEditar)
        
        if frEditar.is_valid():
            frEditar.save()
        else:
            ctxtPOST = {
                'form': frEditar,
                'titulo': 'Editar Centro De formacion - Corregir Errores'
            }
            for mensaje in frEditar.errors:
                messages.error(request, frEditar.errors[mensaje])
                return render(request, 'CFP/centrosForm.html', ctxtPOST)
        
        return redirect('/centros')



@login_required
def centroBorrar(request, idCentro):
    cenBorrar = CentroDeFormacion.objects.get(pk=idCentro)
    cenBorrar.delete()
    return redirect('/centros')
#endregion Centros De Formacion



#region Cursos
@login_required
def cursoNuevo(request):
    if request.user.is_superuser:
        
        formCurso = frmCursos
        ctxt = {
            'form': formCurso,
            'titulo': 'Nuevo Curso'
        }

        if request.method == 'POST':
            formPost = frmCursos(request.POST)

            if formPost.is_valid():
                #formPost.save()
                
                dias = request.POST.getlist('dias')
                fIni = request.POST.getlist('horaInicio')
                fFin = request.POST.getlist('horaFin')
                
                cursoNuevo = Curso()
                cursoNuevo.nombre = request.POST.get('nombre')
                cursoNuevo.cenForm = CentroDeFormacion.objects.get(pk=request.POST.get('cenForm'))
                cursoNuevo.cantHoras = request.POST.get('cantHoras')
                cursoNuevo.fechaInicio = request.POST.get('fechaInicio')
                cursoNuevo.fechaFin = request.POST.get('fechaFin')
                # Asigno Profesor
                pid = request.POST.get('profesor')
                if pid != '':
                    cursoNuevo.profesor = Profesor.objects.get(pk=pid)
                
                #region Checkbox
                # Compruebo el valor de los checboxes
                # Si están seleccionados en el formulario llega por POST
                # una variable con el nombre del campo. Sino, no llega
                # la variable es porque no fue seleccionado, por eso
                # solo compruebo que llegue la variable y no su valor
                #endregion
                if request.POST.get('inscAbierta'):
                    cursoNuevo.inscAbierta = True
                
                if request.POST.get('habilitado'):
                    cursoNuevo.habilitado = True

                if request.POST.get('practico'):
                    cursoNuevo.practico = True
                
                cursoNuevo.save()

                for i in range(len(dias)):
                    nuevoDiaHora = cursoNuevo.diasHorarios.create(dia=dias[i], horaInicio=fIni[i], horaFin=fFin[i])
                
                return redirect('/cursos')
            else:
                for mensaje in formPost.errors:
                    messages.error(request, formPost.errors[mensaje])
                    return render(request, 'CFP/cursosForm.html', {'form': formPost, 'titulo': 'Nuevo Curso'})
        
        else:
            return render(request, 'CFP/cursosForm.html', ctxt)

    else:
        return HttpResponse('Solo disponible para usuario Administrador')



@login_required
def cursoLista(request):
    
    ctxt = {
        'cursos' : Curso.objects.all()
    }
    
    return render(request, 'CFP/cursos.html', ctxt)


@login_required
def cursoEditar(request, idCurso):
    curso = Curso.objects.get(pk=idCurso)
    frEditar = frmCursos()

    if request.method == 'GET':
        frEditar = frmCursos(instance=curso)
        
        ctxGET = {
            'form':frEditar,
            'curso': curso,
            'titulo':'Editar Curso'
        }
        return render(request, 'CFP/cursosFormEdit.html', ctxGET)
    
    #POST
    else:
        dias = request.POST.getlist('dias')
        fIni = request.POST.getlist('horaInicio')
        fFin = request.POST.getlist('horaFin')
        frEditar = frmLocalidad(request.POST, instance=curso)
        
        if frEditar.is_valid():
            #Obtengo el Profesor seleccionado en el form
            comboProfe = request.POST.get('profesor')
            if comboProfe != '':            
                #Asigno al curso el profesor filtrado por id
                profe = Profesor.objects.get(pk=comboProfe)
                curso.profesor = profe
            else:
                curso.profesor = None

            #checkboxes
            if request.POST.get('inscAbierta'):
                curso.inscAbierta = True
            else:
                curso.inscAbierta = False

            if request.POST.get('habilitado'):
                curso.habilitado = True
            else:
                curso.habilitado = False

            if request.POST.get('practico'):
                curso.practico = True
            else:
                curso.practico = False
            
            
            #Editar Dias y Horas
            if len(dias)!=0:
                dhs = curso.diasHorarios.all()
                for dh in dhs:
                    dh.delete()
                for i in range(len(dias)):
                    nuevoDiaHora = curso.diasHorarios.create(dia=dias[i], horaInicio=fIni[i], horaFin=fFin[i])
                frEditar.save()
                #return HttpResponse(dhs)
            else:
                frEditar.save()

            return redirect('/cursos')
        
        # Si el form no es valido
        else:
            ctxtPOST = {
                'form': frEditar,
                'titulo': 'Editar Curso - Corregir Errores'
            }
            for mensaje in frEditar.errors:
                messages.error(request, frEditar.errors[mensaje])
                return render(request, 'CFP/cursosFormEdit.html', ctxtPOST)
        
        return redirect('/cursos')


@login_required
def inscCurso(request, cId):
    if request.user.es_alumno:
        alu = Alumno.objects.get(pk=request.user.id)
        cur = Curso.objects.get(pk=cId)
        insc = CursoAlumno(
            alumno = alu,
            curso = cur
        )
        insc.save()
        return redirect('home')
    else:
        return HttpResponse('no es alumno')


#endregion Cursos