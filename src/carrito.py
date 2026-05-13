"""
Módulo: carrito.py
Clase que gestiona el carrito de compras del usuario.
"""

from src.producto import Producto


class Carrito:
    """Gestiona los ítems agregados por el usuario y calcula subtotales."""

    def __init__(self):
        self._items: dict[str, dict] = {}  # { nombre: {producto, cantidad} }

    def agregar_producto(self, producto: Producto, cantidad: int = 1):
        """Agrega un producto al carrito. Si ya existe, suma la cantidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if not producto.tiene_stock():
            raise ValueError(f"El producto '{producto.nombre}' no tiene stock.")
        if cantidad > producto.stock:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, solicitado: {cantidad}"
            )

        if producto.nombre in self._items:
            self._items[producto.nombre]["cantidad"] += cantidad
        else:
            self._items[producto.nombre] = {"producto": producto, "cantidad": cantidad}

    def quitar_producto(self, nombre: str):
        """Elimina completamente un producto del carrito."""
        if nombre not in self._items:
            raise KeyError(f"El producto '{nombre}' no está en el carrito.")
        del self._items[nombre]

    def calcular_subtotal(self) -> float:
        """Calcula el subtotal sin descuentos ni envío."""
        return sum(
            item["producto"].precio * item["cantidad"]
            for item in self._items.values()
        )

    def cantidad_items(self) -> int:
        """Devuelve el total de unidades en el carrito."""
        return sum(item["cantidad"] for item in self._items.values())

    def esta_vacio(self) -> bool:
        return len(self._items) == 0

    def vaciar(self):
        self._items.clear()

    def obtener_items(self) -> dict:
        return dict(self._items)

    def __repr__(self):
        return f"Carrito({len(self._items)} productos, subtotal=${self.calcular_subtotal():.2f})"
