from django.shortcuts import render
from .models import Usuario

def inicio(request):
    return render(request, 'index.html')

def usuarios(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        rol = request.POST.get('rol')

        Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            rol=rol
        )

    lista_usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': lista_usuarios})
from django.shortcuts import redirect

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('/usuarios/')
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsuarioSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def api_usuarios(request):

    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PUT':
        usuario = Usuario.objects.get(id=request.data['id'])
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        usuario = Usuario.objects.get(id=request.data['id'])
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado"})