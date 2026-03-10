from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre