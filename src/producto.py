"""
Módulo: producto.py
Clase que representa un producto del catálogo.
"""


class Producto:
    """Representa un producto con nombre, precio y stock disponible."""

    def __init__(self, nombre: str, precio: float, stock: int):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.nombre = nombre.strip()
        self.precio = precio
        self.stock = stock

    def tiene_stock(self) -> bool:
        """Devuelve True si hay al menos una unidad disponible."""
        return self.stock > 0

    def reducir_stock(self, cantidad: int):
        """Reduce el stock en la cantidad indicada."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0.")
        if cantidad > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= cantidad

    def __repr__(self):
        return f"Producto(nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"
