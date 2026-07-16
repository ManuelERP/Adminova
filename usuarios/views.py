from django.shortcuts import render, redirect
from .models import Usuario

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsuarioSerializer


def inicio(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    lista_usuarios = Usuario.objects.all()

    contexto = {
        'usuarios': lista_usuarios
    }

    return render(request, 'dashboard.html', contexto)


@login_required
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


@login_required
def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('/usuarios/')


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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')