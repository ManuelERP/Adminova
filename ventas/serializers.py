from rest_framework import serializers

from .models import Venta, DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'total', 'cliente', 'detalles']
        read_only_fields = ['fecha', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')

        venta = Venta.objects.create(**validated_data)

        total = 0

        for detalle_data in detalles_data:
            detalle = DetalleVenta.objects.create(venta=venta, **detalle_data)
            total += detalle.subtotal

        venta.total = total
        venta.save()

        return venta
