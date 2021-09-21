from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from .models import Localidad, CentroDeFormacion

class frmLocalidad(ModelForm):
    class Meta:
        model = Localidad
        fields = '__all__'



class frmCentroFormacion(ModelForm):
    class Meta:
        model = CentroDeFormacion
        fields = '__all__'