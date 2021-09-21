from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from CFP.forms import frmCentroFormacion, frmLocalidad
from django.contrib import messages
from .models import CentroDeFormacion, Localidad
# Create your views here.


def home(request):
    return render(request, 'CFP/home.html')

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
        'centrosForm' : CentroDeFormacion.objects.all(),
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



