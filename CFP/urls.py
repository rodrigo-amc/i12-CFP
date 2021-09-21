from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    #Localidades
    path('localidadNueva', views.localidadNueva, name='localidadNueva'),
    path('localidades', views.localidades, name='localidades'),
    path('localidadEditar/<int:idLocalidad>', views.localidadEditar, name='localidadEditar'),
    path('localidadBorrar/<int:idLocalidad>', views.localidadBorrar, name='localidadBorrar')

]