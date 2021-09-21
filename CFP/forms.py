from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from .models import Localidad

class frmLocalidad(ModelForm):
    class Meta:
        model = Localidad
        fields = '__all__'