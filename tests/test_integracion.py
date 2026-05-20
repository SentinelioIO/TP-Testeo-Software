"""
SPRINT 2 — Prueba de Integración
Verifica que los módulos interactúen correctamente entre sí.
"""

import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.producto import Producto
from src.carrito import Carrito
from src.gestor_descuentos import GestorDescuentos
from src.procesador_pedido import ProcesadorPedido


class TestIntegracionCarritoDescuento(unittest.TestCase):
    """Verifica que Carrito y GestorDescuentos trabajen juntos correctamente."""

    def setUp(self):
        self.carrito = Carrito()
        self.gestor = GestorDescuentos()
        self.producto_a = Producto("Remera", 500.0, 10)
        self.producto_b = Producto("Pantalon", 800.0, 5)

    def test_subtotal_con_multiples_productos_y_descuento_vip(self):
        self.carrito.agregar_producto(self.producto_a, 2)  # 1000
        self.carrito.agregar_producto(self.producto_b, 1)  # 800
        subtotal = self.carrito.calcular_subtotal()        # 1800
        total = self.gestor.aplicar_descuento(subtotal, es_vip=True)
        # VIP + monto > 1000 = 15% descuento → 1800 * 0.85 = 1530
        self.assertAlmostEqual(total, 1530.0)

    def test_subtotal_sin_descuento_cliente_normal_bajo_500(self):
        self.carrito.agregar_producto(self.producto_a, 1)  # 500
        subtotal = self.carrito.calcular_subtotal()
        total = self.gestor.aplicar_descuento(subtotal, es_vip=False)
        self.assertAlmostEqual(total, 500.0)  # sin descuento

    def test_agregar_mismo_producto_dos_veces_acumula(self):
        self.carrito.agregar_producto(self.producto_a, 2)
        self.carrito.agregar_producto(self.producto_a, 3)
        self.assertEqual(self.carrito.cantidad_items(), 5)


class TestIntegracionProcesadorPedido(unittest.TestCase):
    """Verifica el flujo completo a través del ProcesadorPedido."""

    def setUp(self):
        self.procesador = ProcesadorPedido()
        self.carrito = Carrito()
        self.producto = Producto("Zapatillas", 3000.0, 5)

    def test_pedido_vip_envio_gratis_por_monto(self):
        self.carrito.agregar_producto(self.producto, 1)  # 3000
        resultado = self.procesador.procesar(self.carrito, es_vip=True, tipo_envio="estandar")
        # 3000 * 0.85 = 2550 → supera 2000 → envío gratis
        self.assertEqual(resultado["costo_envio"], 0.0)
        self.assertAlmostEqual(resultado["total_final"], 2550.0)

    def test_pedido_no_vip_con_envio_express(self):
        p = Producto("Gorra", 300.0, 10)
        self.carrito.agregar_producto(p, 1)
        resultado = self.procesador.procesar(self.carrito, es_vip=False, tipo_envio="express")
        self.assertEqual(resultado["costo_envio"], 1000.0)
        self.assertAlmostEqual(resultado["total_final"], 1300.0)

    def test_carrito_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            self.procesador.procesar(self.carrito, es_vip=False, tipo_envio="estandar")

    def test_tipo_envio_invalido_lanza_error(self):
        self.carrito.agregar_producto(self.producto, 1)
        with self.assertRaises(ValueError):
            self.procesador.procesar(self.carrito, es_vip=False, tipo_envio="helicoptero")


if __name__ == "__main__":
    unittest.main(verbosity=2)
