"""
tests/test_e2e.py
Pruebas End-to-End (E2E) — Sprint 4
"""

import pytest
from src.producto import Producto
from src.carrito import Carrito
from src.gestor_descuentos import GestorDescuentos
from src.procesador_pedido import ProcesadorPedido


class TestE2EFlujoBasico:
    """E2E-01: Cliente no VIP, un solo producto, envío estándar."""

    def test_compra_simple_cliente_normal(self):
        producto = Producto("Teclado", 800.0, stock=10)
        carrito = Carrito()
        procesador = ProcesadorPedido()

        carrito.agregar_producto(producto, cantidad=1)
        resultado = procesador.procesar(carrito, es_vip=False, tipo_envio="estandar")

        assert resultado["subtotal"] == 800.0
        assert resultado["porcentaje_descuento"] == 0.03
        assert resultado["total_con_descuento"] == 776.0
        assert resultado["costo_envio"] == 500.0
        assert resultado["total_final"] == 1276.0


class TestE2EFlujoVIP:
    """E2E-02: Cliente VIP, múltiples productos, descuento máximo 15%."""

    def test_compra_vip_descuento_maximo(self):
        notebook = Producto("Notebook", 1500.0, stock=5)
        mouse = Producto("Mouse", 300.0, stock=20)
        carrito = Carrito()
        procesador = ProcesadorPedido()

        carrito.agregar_producto(notebook, cantidad=1)
        carrito.agregar_producto(mouse, cantidad=2)
        resultado = procesador.procesar(carrito, es_vip=True, tipo_envio="estandar")

        # subtotal = 1500 + 600 = 2100
        # descuento = 15% (VIP 10% + monto>1000 5%)
        # total_con_descuento = 2100 * 0.85 = 1785
        # 1785 < 2000 → envío NO es gratis
        assert resultado["subtotal"] == 2100.0
        assert resultado["porcentaje_descuento"] == 0.15
        assert resultado["total_con_descuento"] == 1785.0
        assert resultado["costo_envio"] == 500.0
        assert resultado["total_final"] == 2285.0


class TestE2EFlujoEnvioGratis:
    """E2E-03: Envío gratis cuando total con descuento supera $2000."""

    def test_envio_gratis_subtotal_alto(self):
        tv = Producto("TV", 3000.0, stock=3)
        carrito = Carrito()
        procesador = ProcesadorPedido()

        carrito.agregar_producto(tv, cantidad=1)
        resultado = procesador.procesar(carrito, es_vip=False, tipo_envio="estandar")

        # subtotal = 3000, descuento 3% → 2910
        # 2910 >= 2000 → envío gratis
        assert resultado["subtotal"] == 3000.0
        assert resultado["total_con_descuento"] == 2910.0
        assert resultado["costo_envio"] == 0.0
        assert resultado["total_final"] == 2910.0


class TestE2EFlujoExpress:
    """E2E-04: Cliente no VIP, envío express."""

    def test_compra_con_envio_express(self):
        auriculares = Producto("Auriculares", 400.0, stock=15)
        funda = Producto("Funda", 150.0, stock=30)
        carrito = Carrito()
        procesador = ProcesadorPedido()

        carrito.agregar_producto(auriculares, cantidad=1)
        carrito.agregar_producto(funda, cantidad=1)
        resultado = procesador.procesar(carrito, es_vip=False, tipo_envio="express")

        # subtotal = 550, descuento 3% → 533.5, envío express 1000
        assert resultado["subtotal"] == 550.0
        assert resultado["porcentaje_descuento"] == 0.03
        assert resultado["costo_envio"] == 1000.0
        assert resultado["total_final"] == 1533.5


class TestE2EFlujoCarritoVacio:
    """E2E-05: Carrito vacío debe lanzar error."""

    def test_error_carrito_vacio(self):
        carrito = Carrito()
        procesador = ProcesadorPedido()

        with pytest.raises(ValueError, match="carrito vacío"):
            procesador.procesar(carrito, es_vip=False, tipo_envio="estandar")


class TestE2EFlujoStockInsuficiente:
    """E2E-06: Stock insuficiente debe lanzar error."""

    def test_error_stock_insuficiente(self):
        producto = Producto("Monitor", 2000.0, stock=2)
        carrito = Carrito()

        with pytest.raises(ValueError, match="Stock insuficiente"):
            carrito.agregar_producto(producto, cantidad=5)


class TestE2EFlujoQuitarProducto:
    """E2E-07: Agregar productos, quitar uno y procesar."""

    def test_quitar_producto_y_procesar(self):
        silla = Producto("Silla", 900.0, stock=5)
        lampara = Producto("Lampara", 300.0, stock=10)
        carrito = Carrito()
        procesador = ProcesadorPedido()

        carrito.agregar_producto(silla, cantidad=1)
        carrito.agregar_producto(lampara, cantidad=1)
        carrito.quitar_producto("Lampara")
        resultado = procesador.procesar(carrito, es_vip=False, tipo_envio="estandar")

        assert resultado["subtotal"] == 900.0
        assert resultado["porcentaje_descuento"] == 0.03
        assert resultado["total_con_descuento"] == 873.0
        assert resultado["costo_envio"] == 500.0
        assert resultado["total_final"] == 1373.0