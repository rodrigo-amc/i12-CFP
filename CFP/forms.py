from django import forms
from django.db import models
from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import Curso, Localidad, CentroDeFormacion, diaHora

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
            'habilitado',
            'practico',
            'cantHoras',
            'fechaInicio',
            'fechaFin',
        ]

        labels = {
            'nombre':'Nombre',
            'cenForm':'Centro De Formacion',
            'practico':'Curso Practico',
            'cantHoras':'Cantidad De Horas',
            'fechaInicio':'Fecha De Inicio',
            'fechaFin':'Fecha De Finalizacion'
        }

        widgets = {
            'fechaInicio' : widgetFecha(),
            'fechaFin' : widgetFecha()
        }
