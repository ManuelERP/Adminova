from django.contrib import admin
from django.urls import path
from usuarios.views import inicio, usuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('usuarios/', usuarios),
]