from django.urls import path
from Usuarios import views

urlpatterns = [
    path('', views.logIn, name='login'),
    path('menu', views.menu, name='menu')
]
