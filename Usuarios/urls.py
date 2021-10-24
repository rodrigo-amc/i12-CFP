from django.urls import path
from Usuarios import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.logIn, name='login'),
    path('menu', views.menu, name='menu'),
    path('crearAlumno', views.crearAlumno, name='crearAlumno')
]

# Ruta para las imagenes
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)