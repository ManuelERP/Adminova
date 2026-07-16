from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cliente


@login_required
def clientes(request):

    if request.method == 'POST':

        Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            tipo_documento=request.POST.get('tipo_documento'),
            numero_documento=request.POST.get('numero_documento'),
            telefono=request.POST.get('telefono'),
            correo=request.POST.get('correo'),
            direccion=request.POST.get('direccion'),
        )

    lista_clientes = Cliente.objects.all()

    contexto = {
        'clientes': lista_clientes,
        'total_clientes': lista_clientes.count(),
    }

    return render(request, 'clientes.html', contexto)


@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.tipo_documento = request.POST.get('tipo_documento')
        cliente.numero_documento = request.POST.get('numero_documento')
        cliente.telefono = request.POST.get('telefono')
        cliente.correo = request.POST.get('correo')
        cliente.direccion = request.POST.get('direccion')
        cliente.save()

        return redirect('/clientes/')

    contexto = {
        'cliente': cliente
    }

    return render(request, 'editar_cliente.html', contexto)


@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('/clientes/')
