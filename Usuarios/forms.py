from django import forms
#from django.forms import ModelForm

from .models import appUser, Alumno

#Widgets
class widgetFecha(forms.DateInput):
    input_type = 'date'



#Forms
class frmAlumno(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'Dni',
            'fecha_nacimiento',
            'DniImg',
            'Autorizacion',
            'Telefono',
            'Domicilio',
            'localidad',
        ]

        widgets = {
            'fecha_nacimiento' : widgetFecha()
        }

        labels = {
            'fecha_nacimiento' : 'Fecha De Nacimiento',
            'DniImg' : 'Foto DNI',
            'localidad': 'Localidad'
        }



class frmUsuario(forms.ModelForm):
    class Meta:
        model = appUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]

        labels = {
            'first_name' : 'Nombre',
            'last_name' : 'Apellido',
            'email' : 'Correo Electronico',
            'password': 'Contraseña'
        }

        widgets = {
            'password' : forms.PasswordInput()
        }