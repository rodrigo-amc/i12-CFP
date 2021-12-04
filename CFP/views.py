from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from CFP.forms import frmCentroFormacion, frmCursos, preFrmCursos, frmLocalidad
from django.contrib import messages

from Usuarios.models import Alumno, CursoAlumno, Profesor, appUser
from .models import CentroDeFormacion, Curso, Localidad
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
        'alumno' : amno,
        
    }
    return render(request, 'CFP/homePrincipal.html', ctxtHome)



#region CRUD Localidades
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



#region CRUD Centros De Formacion
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

#endregion Centros De Formacion



#region CRUD Cursos
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
                cursoNuevo.cupoMin = request.POST.get('cupoMin')
                cursoNuevo.cupoMax = request.POST.get('cupoMax')
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
    if request.user.is_superuser:
        cursos = Curso.objects.all().order_by('-cenForm')
        ctx = {
            'cursos': cursos,
            'titulo': 'Listado De Cursos'
        }
        return render(request, 'CFP/cursosCRUD.html', ctx)
    else:
        return redirect('home')



@login_required
def cursoInfo(request):
    if request.user.is_superuser:    
        cursos = Curso.objects.all().order_by('-cenForm')


        ctxt = {
            'cursos' : cursos,
            'titulo': 'Informe De Cursos'
        }
        
        """ for c in cursos:
            print('----------------------------')
            print('CFP: {0}'.format(c.cenForm))
            print('Curso: {0}'.format(c))
            for ca in csoal:
                if ca.curso == c:
                    print('Alumno: {0}'.format(ca.alumno))
                    print('********* FIN *********') """
        
        """ for c in cursos:
            als =c.alumno_set.all()
            print('---------------------------------')
            print('Curso: {0}'.format(c))
            print(als)
            for a in als:
                csoal = a.cursoalumno_set.all().filter(curso = c)
                print(csoal)
            aprobados = c.cursoalumno_set.filter(aprobado=True)
            print('Curso: {0}'.format(c.id))
            print('Aprobados: {0}'.format(len(aprobados)))
            print('------------------------------------') """

        return render(request, 'CFP/cursosInforme.html', ctxt)
    else:
        return redirect('home')



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
#endregion Cursos



@login_required
def adminInfoAlumnos(request):
    if request.user.is_superuser:
        
        inscriptos = []
        sinCurso = []
        alumnos = Alumno.objects.all()

        for a in alumnos:
            if (a not in inscriptos) and (a not in sinCurso):
                
                if len(a.cursoalumno_set.all()) != 0 :
                    inscriptos.append(a)
                else:
                    sinCurso.append(a)


        for i in inscriptos:
            print(i.usr_alumno.last_name)
        
        print('{0} Sin Curso {0}'.format('---------------'))
        for s in sinCurso:
            print(s.usr_alumno.last_name)


        ctxt = {
            'cursando': inscriptos,
            'sincurso': sinCurso,
            'titulo': "Informe De Alumnos"
        }

        return render(request, 'CFP/alumnosLst.html', ctxt)


#Alumno
@login_required
def misCursos(request):
    #region LEEME CursoAlumno
    # En el template accedo a los cursos del alumno a traves
    # del modelo de relacion N a N "CursoAlumno". "curso" es
    # un campo en el modelo "Alumno" que establece la relacion
    # N a N entre "Alumno" y "Curso" a traves del modelo
    # "AlumnoCurso". Como el campo de la relacion se
    # establece en "Alummno", solo puedo acceder a
    # este desde "Alumno" y no desde "Curso"
    # (Ver modelos para entender)
    # Lo hago asi para poder acceder a los campos de "AlumnoCurso"
    # porcAsist, notaCurso y aprobado
    #endregion
    
    user = request.user
    
    if user.es_alumno:
        alumno = Alumno.objects.get(pk=request.user.id)

        aluCtxt={
            'usuario' : user,
            'alumno' : alumno,
            'titulo' : 'Menu Alumno',
            'miscursos':'Todos Los Cursos'
        }
        
        # miscursos
        # paso la variable para levantarla en el header que hereda
        # el template#

        return render(request, 'CFP/homeAlumno.html', aluCtxt)
    else:
        return redirect('home')



#Alumno
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
        messages.success(request, 'Te Inscribiste Al Curso {0}'.format(cur))
        return redirect('home')
    else:
        return HttpResponse('no es alumno')



#region Preceptor Funciones
@login_required
def preLstCursos(request):
    '''Preceptor Listado De Cursos'''
    
    if request.user.es_preceptor:
        
        #usuario logueado
        usr = request.user
        
        #CFP asociado al preceptor
        preCfp = usr.preceptor.cfp

        #Cursos asociados al CFP del preceptor
        preCursos = Curso.objects.all().filter(cenForm=preCfp)
        

        ctxt = {
            'cfp' : preCfp,
            'cursos' : preCursos,
            'usuario' : usr,
            'titulo' : 'Cursos'
        }
        
        return render(request, 'CFP/preCursoLst.html', ctxt)

    else:
        return redirect('home')



#region Prec CRUD Cursos
@login_required
def preCursoNuevo(request):
    if request.user.es_preceptor:
        usr = request.user
        preCenFor = usr.preceptor.cfp
        formCurso = preFrmCursos()
        
        ctxt = {
            'form': formCurso,
            'titulo': str(preCenFor)+' Nuevo Curso'
        }

        if request.method == 'POST':
            formPost = preFrmCursos(request.POST)

            if formPost.is_valid():
                #formPost.save()
                
                dias = request.POST.getlist('dias')
                fIni = request.POST.getlist('horaInicio')
                fFin = request.POST.getlist('horaFin')
                
                cursoNuevo = Curso()
                cursoNuevo.nombre = request.POST.get('nombre')
                cursoNuevo.cenForm = CentroDeFormacion.objects.get(pk=preCenFor.id)
                cursoNuevo.cantHoras = request.POST.get('cantHoras')
                cursoNuevo.fechaInicio = request.POST.get('fechaInicio')
                cursoNuevo.fechaFin = request.POST.get('fechaFin')
                cursoNuevo.cupoMin = request.POST.get('cupoMin')
                cursoNuevo.cupoMax = request.POST.get('cupoMax')
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
                
                return redirect('/preLstCursos')
            else:
                for mensaje in formPost.errors:
                    messages.error(request, formPost.errors[mensaje])
                    print(mensaje)
                    return render(request, 'CFP/preCursoForm.html', {'form': formPost, 'titulo': 'Nuevo Curso ERRORES'})
        
        else:
            return render(request, 'CFP/preCursoForm.html', ctxt)

    else:
        return HttpResponse('Solo disponible para usuario Administrador')



@login_required
def preCursoEditar(request, idCurso):
    if request.user.es_preceptor:
        cenFor = request.user.preceptor.cfp
        curso = Curso.objects.get(pk=idCurso)
        frEditar = preFrmCursos()

        if request.method == 'GET':
            frEditar = preFrmCursos(instance=curso)
            
            ctxGET = {
                'form':frEditar,
                'curso': curso,
                'titulo': str(cenFor)+' Editar Curso'
            }
            return render(request, 'CFP/preCursoFormEdit.html', ctxGET)
        
        #POST
        else:
            dias = request.POST.getlist('dias')
            fIni = request.POST.getlist('horaInicio')
            fFin = request.POST.getlist('horaFin')
            frEditar = preFrmCursos(request.POST, instance=curso)
            
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

                return redirect('/preLstCursos')
            
            # Si el form no es valido
            else:
                ctxtPOST = {
                    'form': frEditar,
                    'titulo': str(cenFor)+' Editar Curso - Corregir Errores'
                }
                for mensaje in frEditar.errors:
                    messages.error(request, frEditar.errors[mensaje])
                    return render(request, 'CFP/preCursoFormEdit.html', ctxtPOST)
            
            return redirect('/preLstCursos')
    
    #Si el usuario no es preceptor
    else:
        return redirect('/home')

#endregion

#region Prec Listar Alumnos
@login_required
def preLstAlu(request):
    '''Lista Todos Los Alumnos Relacionados al Centro
    De Formacion Al Que Pertenece El Preceptor'''
    if request.user.es_preceptor:

        # Obtengo el cfp al que pertenece el preceptor
        preCfp = request.user.preceptor.cfp

        #Obtengo Todos los alumnos
        alumnos = Alumno.objects.all()

        #Lista en la que solo estan los alumnos relacionados
        # al cfp relacionado con el preceptor
        alsCfp = []

        # Itero sobre los alumnos
        for a in alumnos:
            #itero sobre los cursos del alumno
            for c in a.curso.all():
                #si el curso pertenece al cfp del preceptor
                if c.cenForm == preCfp:
                    #si el alumno ya esta en la lista "alsCfp"
                    if a in alsCfp:
                        #saltea
                        pass
                    #sino lo agrega a la lista "alsCfp"
                    else:
                        alsCfp.append(a)

        ctxt = {
            'centroform': preCfp,
            'alumnos': alsCfp,
            'titulo': str(preCfp)+' Alumnos'
        }
            
        return render(request, 'CFP/preLstAlumnos.html', ctxt)
    else:
        return redirect('home')


@login_required
def preVerAlumno(request, aluID):
    if request.user.es_preceptor:
        alumno = Alumno.objects.get(pk = aluID)
        ctx = {
            'alu':alumno,
            'titulo': 'Datos Del Alumno '+str(alumno.usr_alumno.first_name)+' '+str(alumno.usr_alumno.last_name)
        }
        
        return render(request, 'CFP/preVerAlumno.html', ctx)
    else:
        return redirect('home')
#endregion

#region Prec Notas y Asistencias
@login_required
def preNotAsi(request, cId):
    '''Controlador para asignar notas y asistencias del curso'''
    if request.user.es_preceptor:
        
        # Obtengo el usuario logueado
        usr = request.user

        #Ontengo el curso seleccionado en template
        cursoSelect = Curso.objects.get(pk=cId)

        """#Obtengo todos los alumnos relacionados a este curso
        #Recordar que en la relacion N a N, Alumno tiene el
        #campo "curso", pero curso NO tiene campo "Alumno"
        #por eso accedo con "_set.all()"
        alsCso = cursoSelect.alumno_set.all()"""
        
        
        #PROBANDO CON cursoalumno
        #OJO NO ENVIAR ALUMNOS CON "APROBADO"==True
        curso_Alumno = CursoAlumno.objects.filter(curso = cursoSelect)

        ctxt = {
                'usuario': usr,
                'cuAl': curso_Alumno,
                'idCurso': cId,
                'titulo': str(cursoSelect)+ ': Notas y Asistencias'
            }        
            


        if request.method == 'POST':
            csoAls = request.POST.getlist('cursoalumno')
            asistencias = request.POST.getlist('asistCurso')
            notas = request.POST.getlist('notaCurso')

            for i in range(len(csoAls)):
                ca = CursoAlumno.objects.get(pk = csoAls[i])
                ca.porcAsist = asistencias[i]
                ca.notaCurso = notas[i]

                #Si checkbox aprobado
                if request.POST.get('aprobado'+str(ca.id)):
                    print('aprobado'+str(ca.id))
                    ca.aprobado = True
                ca.save()
                print('**********************************')
            return render(request, 'CFP/preNotasAsistencia.html', ctxt)

        else:
            
            return render(request, 'CFP/preNotasAsistencia.html', ctxt)
    
    # Si No es preceptor
    else:
        return redirect('home')
#endregion

#endregion