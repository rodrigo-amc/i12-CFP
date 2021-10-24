from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import appUser, Alumno


#admin.site.register(appUser)
#Esta clase me permite editar los campos que se muestran en el panel de administracion.
#Con el decorador "@admin.register" le indico con que modelo tiene que trabajar.
#Para que se encripte la contraseña hay que heredar de UserAdmin, pero esto hace que
#no se muestren todos los campos, por eso tengo que usar el fieldset.
@admin.register(appUser)
class usuarioAdmin(UserAdmin):
    list_display = ('username','first_name', 'last_name', )
    

    fieldsets = (
        ('User Data', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'username',
                'password',
            )
        }),

        ('Security', {
            'fields': (
                'is_superuser',
                'is_staff',
                'is_active',
            ),
        }),

        ('Rol', {
            'fields': (
                'es_alumno',
                'es_profesor',
            ),
        }),
    )


#admin.site.register(Alumno)
@admin.register(Alumno)
class alumnoAdmin(admin.ModelAdmin):
    pass

