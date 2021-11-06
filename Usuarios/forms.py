from django import forms
from .models import appUser, Alumno, Profesor

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



    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if len(nombre)<3:
            raise forms.ValidationError('Por favor ingresa un nombre con al menos 3 letras')
        else:
            return nombre

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if len(apellido)<3:
            raise forms.ValidationError('Por favor ingresa un apellido con al menos 3 letras')
        else:
            return apellido



class frmProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['telefono']



class frmUsrProf(forms.ModelForm):
    class Meta:
        model = appUser
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'first_name' : 'Nombre',
            'last_name' : 'Apellido',
            'email' : 'Correo Electronico'
        }

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if len(nombre)<3:
            raise forms.ValidationError('Por favor ingresa un nombre con al menos 3 letras')
        else:
            return nombre

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if len(apellido)<3:
            raise forms.ValidationError('Por favor ingresa un apellido con al menos 3 letras')
        else:
            return apellido