from django import forms
from django.forms import ModelForm

from .models import Curso, Localidad, CentroDeFormacion

class frmLocalidad(ModelForm):
    class Meta:
        model = Localidad
        fields = '__all__'



class frmCentroFormacion(ModelForm):
    class Meta:
        model = CentroDeFormacion
        fields = '__all__'



class widgetFecha(forms.DateInput):
    input_type = 'date'


class frmCursos(ModelForm):
    class Meta:
        model = Curso

        fields = [
            'nombre',
            'cenForm',
            'profesor',
            'inscAbierta',
            'habilitado',
            'practico',
            'cupoMin',
            'cupoMax',
            'cantHoras',
            'fechaInicio',
            'fechaFin',
        ]

        labels = {
            'nombre':'Nombre',
            'cenForm':'Centro De Formacion',
            'inscAbierta': 'Inscripcion Abierta',
            'practico':'Curso Practico',
            'cupoMin':'Cupo Minimo',
            'cupoMax':'Cupo Maximo',
            'cantHoras':'Cantidad De Horas',
            'fechaInicio':'Fecha De Inicio',
            'fechaFin':'Fecha De Finalizacion'
        }

        widgets = {
            'fechaInicio' : widgetFecha(),
            'fechaFin' : widgetFecha()
        }



#region Preceptor
class preFrmCursos(ModelForm):
    class Meta:
        model = Curso

        fields = [
            'nombre',
            'profesor',
            'inscAbierta',
            'habilitado',
            'practico',
            'cupoMin',
            'cupoMax',
            'cantHoras',
            'fechaInicio',
            'fechaFin',
        ]

        labels = {
            'nombre':'Nombre',
            'inscAbierta': 'Inscripcion Abierta',
            'practico':'Curso Practico',
            'cupoMin':'Cupo Minimo',
            'cupoMax':'Cupo Maximo',
            'cantHoras':'Cantidad De Horas',
            'fechaInicio':'Fecha De Inicio',
            'fechaFin':'Fecha De Finalizacion'
        }

        widgets = {
            'fechaInicio' : widgetFecha(),
            'fechaFin' : widgetFecha()
        }
#endregion
