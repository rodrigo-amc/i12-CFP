"""CentrosDeFormacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Importo el archivo settings para poder trabajar con los
# valores asignados a "MEDIA_URL" y "MEDIA_ROOT"
from django.conf import settings

# Importo los archivos estaticos
# Esto me permite agregar a "urlpatterns"
# la ruta a las imagenes
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CFP.urls')),
    path('', include("Usuarios.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)