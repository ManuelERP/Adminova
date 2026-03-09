from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre