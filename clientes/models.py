from django.db import models


class Cliente(models.Model):
    CC = 'CC'
    NIT = 'NIT'
    TIPO_DOCUMENTO_CHOICES = [
        (CC, 'Cédula de Ciudadanía'),
        (NIT, 'NIT'),
    ]

    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default=CC)
    numero_documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
