from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('misCursos', views.misCursos, name='misCursos'),

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
    path('cursoEditar/<int:idCurso>', views.cursoEditar, name='cursoEditar'),
    path('inscCurso/<int:cId>', views.inscCurso, name='inscCurso'),

    #Preceptor Cursos
    path('preLstCursos', views.preLstCursos, name='preLstCursos'),
    path('preCursoNuevo', views.preCursoNuevo, name='preCursoNuevo'),
    path('preCursoEditar/<int:idCurso>', views.preCursoEditar, name='preCursoEditar'),
    path('preLstAlu', views.preLstAlu, name='preLstAlu'),
    path('preVerAlumno/<int:aluID>', views.preVerAlumno, name='preVerAlumno'),
    path('preNotAsi/<int:cId>', views.preNotAsi, name='preNotAsi'),
]