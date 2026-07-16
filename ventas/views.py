from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from clientes.models import Cliente
from productos.models import Producto
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer


CARRITO_SESSION_KEY = 'carrito_venta'


def _guardar_carrito(request, carrito):
    request.session[CARRITO_SESSION_KEY] = carrito
    request.session.modified = True


@login_required
def ventas(request):

    carrito = request.session.get(CARRITO_SESSION_KEY, {})

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'agregar':
            producto_id = request.POST.get('producto_id')
            cantidad = int(request.POST.get('cantidad', 0))

            producto = get_object_or_404(Producto, id=producto_id)
            cantidad_actual = carrito.get(producto_id, 0)

            if cantidad > 0 and (cantidad_actual + cantidad) <= producto.stock:
                carrito[producto_id] = cantidad_actual + cantidad
                _guardar_carrito(request, carrito)
            else:
                messages.error(request, 'No hay stock suficiente para agregar ese producto.')

        elif accion == 'quitar':
            producto_id = request.POST.get('producto_id')
            carrito.pop(producto_id, None)
            _guardar_carrito(request, carrito)

        elif accion == 'cancelar':
            _guardar_carrito(request, {})

        elif accion == 'finalizar' and carrito:
            productos_cache = {}
            suficiente = True

            for producto_id, cantidad in carrito.items():
                producto = Producto.objects.filter(id=producto_id).first()

                if not producto or cantidad > producto.stock:
                    suficiente = False
                    nombre = producto.nombre if producto else 'un producto'
                    messages.error(request, f'Stock insuficiente para {nombre}.')
                    break

                productos_cache[producto_id] = producto

            if suficiente:
                cliente_id = request.POST.get('cliente_id') or None
                cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None

                with transaction.atomic():
                    venta = Venta.objects.create(total=0, cliente=cliente)
                    total = Decimal('0')

                    for producto_id, cantidad in carrito.items():
                        producto = productos_cache[producto_id]

                        DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=producto.precio,
                        )

                        producto.stock -= cantidad
                        producto.save()

                        total += producto.precio * cantidad

                    venta.total = total
                    venta.save()

                _guardar_carrito(request, {})

        return redirect('/ventas/')

    productos_disponibles = Producto.objects.filter(stock__gt=0)

    items_carrito = []
    total_carrito = Decimal('0')

    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.filter(id=producto_id).first()

        if not producto:
            continue

        subtotal = producto.precio * cantidad
        total_carrito += subtotal

        items_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    contexto = {
        'productos_disponibles': productos_disponibles,
        'clientes_disponibles': Cliente.objects.all(),
        'items_carrito': items_carrito,
        'total_carrito': total_carrito,
        'ventas': Venta.objects.order_by('-fecha'),
    }

    return render(request, 'ventas.html', contexto)


@login_required
def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    venta.delete()
    return redirect('/ventas/')


@login_required
def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    contexto = {
        'venta': venta,
    }

    return render(request, 'detalle_venta.html', contexto)


@api_view(['GET', 'POST', 'DELETE'])
def api_ventas(request):

    if request.method == 'GET':
        lista_ventas = Venta.objects.all()
        serializer = VentaSerializer(lista_ventas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VentaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        venta = get_object_or_404(Venta, id=request.data['id'])
        venta.delete()

        return Response({
            "mensaje": "Venta eliminada correctamente"
        })
