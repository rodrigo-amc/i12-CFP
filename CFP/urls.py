from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    #Localidades
    path('localidadNueva', views.localidadNueva, name='localidadNueva'),
    path('localidades', views.localidades, name='localidades'),
    path('localidadEditar/<int:idLocalidad>', views.localidadEditar, name='localidadEditar'),
    path('localidadBorrar/<int:idLocalidad>', views.localidadBorrar, name='localidadBorrar'),

    #Centros De Formacion
    path('centroNuevo', views.centroNuevo, name='centroNuevo'),
    path('centros', views.centros, name='centros'),
    path('centrosEditar/<int:idCentro>', views.centroEditar, name='centrosEditar'),
    path('centrosBorrar/<int:idCentro>', views.centroBorrar, name='centrosBorrar'),

    #Cursos
    path('cursoNuevo', views.cursoNuevo, name='cursoNuevo'),
    path('cursos', views.cursoLista, name='cursos'),

]