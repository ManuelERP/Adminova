from django.test import TestCase
from .models import Empresa

class EmpresaModelTest(TestCase):

    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre="Adminova SAS",
            nit="900123456-1",
            direccion="Calle 10 # 20-30",
            telefono="3001234567",
            email="contacto@adminova.com",
        )

    def test_creacion_empresa(self):
        self.assertEqual(Empresa.objects.count(), 1)
        self.assertEqual(self.empresa.nit, "900123456-1")

    def test_str_empresa(self):
        self.assertEqual(str(self.empresa), "Adminova SAS")