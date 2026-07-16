from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario
 
class UsuarioModelTest(TestCase):
 
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre="Ana Torres",
            correo="ana.torres@adminova.com",
            telefono="3009876543",
            rol="Administrador",
        )
 
    def test_creacion_usuario(self):
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(self.usuario.rol, "Administrador")
 
    def test_str_usuario(self):
        self.assertEqual(str(self.usuario), "Ana Torres")
 
 
class VistasTest(TestCase):
 
    def setUp(self):
        self.client = Client()
 
    def test_vista_inicio(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
 
    def test_vista_usuarios(self):
        response = self.client.get("/usuarios/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "usuarios.html")
