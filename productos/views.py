from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Producto
from .serializers import ProductoSerializer


@login_required
def productos(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock
        )

    lista_productos = Producto.objects.all()

    total_productos = lista_productos.count()

    total_stock = sum(producto.stock for producto in lista_productos)

    valor_inventario = sum(
        producto.precio * producto.stock
        for producto in lista_productos
    )

    contexto = {
        'productos': lista_productos,
        'total_productos': total_productos,
        'total_stock': total_stock,
        'valor_inventario': valor_inventario,
    }

    return render(request, 'productos.html', contexto)


@login_required
def eliminar_producto(request, id):

    producto = Producto.objects.get(id=id)

    producto.delete()

    return redirect('/productos/')

@login_required
def editar_producto(request, id):

    producto = Producto.objects.get(id=id)

    if request.method == 'POST':

        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')

        producto.save()

        return redirect('/productos/')

    contexto = {
        'producto': producto
    }

    return render(request, 'editar_producto.html', contexto)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def api_productos(request):

    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PUT':

        producto = Producto.objects.get(id=request.data['id'])

        serializer = ProductoSerializer(
            producto,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':

        producto = Producto.objects.get(id=request.data['id'])

        producto.delete()

        return Response({
            "mensaje": "Producto eliminado correctamente"
        })