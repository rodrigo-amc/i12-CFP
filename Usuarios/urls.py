from collections import namedtuple
from django.urls import path
from Usuarios import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.logIn, name='login'),
    path('menu', views.menu, name='menu'),

    #Profesores
    path('profesores', views.lstProfesores, name='profesores'),
    path('crearProfesor', views.crearProfesor, name='crearProfesor'),
    path('editProf/<int:idUsr>', views.editarProfesor, name='editProf'),
    path('deshabProf/<int:idUsr>', views.profDeshabilitar, name='deshabProf'),

    #Preceptores
    path('preceptores', views.lstPreceptores, name='preceptores'),
    path('crearPreceptor', views.crearPreceptor, name='crearPreceptor'),
    path('editPrec/<idUsr>', views.editarPreceptor, name='editPrec'),
    path('deshabPrec/<idUsr>', views.deshabilitarPreceptor, name='deshabPrec'),

    #Alumno
    path('crearAlumno', views.crearAlumno, name='crearAlumno'),
    path('borrarAlumno/<int:aID>', views.borrarAlumno, name='borrarAlumno')
]

# Ruta para las imagenes
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)