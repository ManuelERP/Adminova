from django.contrib import admin
from django.urls import path
from usuarios.views import inicio, usuarios, eliminar_usuario, api_usuarios
from empresas.views import inicio as empresas_inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('usuarios/', usuarios),
    path('empresas/', empresas_inicio),
    path('eliminar/<int:id>/', eliminar_usuario),
    path('api/usuarios/', api_usuarios),
]