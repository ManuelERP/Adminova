from django.contrib import admin
from django.urls import path

from usuarios.views import (
    inicio,
    dashboard,
    usuarios,
    eliminar_usuario,
    api_usuarios,
    login_view,
    logout_view
)

from empresas.views import inicio as empresas_inicio

from productos.views import (
    productos,
    eliminar_producto,
    editar_producto,
    api_productos
)

from ventas.views import (
    ventas,
    eliminar_venta,
    detalle_venta,
    api_ventas
)

from clientes.views import (
    clientes,
    editar_cliente,
    eliminar_cliente
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inicio
    path('', inicio),

    # Autenticación
    path('login/', login_view),
    path('logout/', logout_view),

    # Dashboard
    path('dashboard/', dashboard),

    # Usuarios
    path('usuarios/', usuarios),
    path('eliminar/<int:id>/', eliminar_usuario),

    # Empresas
    path('empresas/', empresas_inicio),

    # Productos
    path('productos/', productos),
    path('editar_producto/<int:id>/', editar_producto),
    path('eliminar_producto/<int:id>/', eliminar_producto),

    # Ventas
    path('ventas/', ventas),
    path('ventas/<int:id>/', detalle_venta),
    path('ventas/eliminar/<int:id>/', eliminar_venta),

    # Clientes
    path('clientes/', clientes),
    path('editar_cliente/<int:id>/', editar_cliente),
    path('eliminar_cliente/<int:id>/', eliminar_cliente),

    # API
    path('api/usuarios/', api_usuarios),
    path('api/productos/', api_productos),
    path('api/ventas/', api_ventas),
]