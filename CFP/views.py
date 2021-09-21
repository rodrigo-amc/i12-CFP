from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from CFP.forms import frmLocalidad
from django.contrib import messages
from .models import Localidad
# Create your views here.


def home(request):
    return render(request, 'CFP/home.html')


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