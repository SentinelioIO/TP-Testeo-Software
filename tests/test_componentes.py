"""
SPRINT 2 — Prueba de Componentes
Verifica cada clase de forma aislada, sin depender de las demás.
"""

import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.producto import Producto
from src.carrito import Carrito
from src.gestor_descuentos import GestorDescuentos


# ─────────────────────────────────────────────
#  Componente: Producto
# ─────────────────────────────────────────────
class TestProducto(unittest.TestCase):

    def test_creacion_valida(self):
        p = Producto("Remera", 1500.0, 10)
        self.assertEqual(p.nombre, "Remera")
        self.assertEqual(p.precio, 1500.0)
        self.assertEqual(p.stock, 10)

    def test_tiene_stock_true(self):
        p = Producto("Remera", 1500.0, 5)
        self.assertTrue(p.tiene_stock())

    def test_tiene_stock_false(self):
        p = Producto("Remera", 1500.0, 0)
        self.assertFalse(p.tiene_stock())

    def test_reducir_stock_valido(self):
        p = Producto("Remera", 1500.0, 10)
        p.reducir_stock(3)
        self.assertEqual(p.stock, 7)

    def test_reducir_stock_insuficiente(self):
        p = Producto("Remera", 1500.0, 2)
        with self.assertRaises(ValueError):
            p.reducir_stock(5)

    def test_precio_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("X", -100.0, 5)

    def test_nombre_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("", 100.0, 5)

    def test_stock_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto("X", 100.0, -1)


# ─────────────────────────────────────────────
#  Componente: Carrito
# ─────────────────────────────────────────────
class TestCarrito(unittest.TestCase):

    def setUp(self):
        self.carrito = Carrito()
        self.producto = Producto("Pantalon", 2000.0, 10)

    def test_carrito_inicia_vacio(self):
        self.assertTrue(self.carrito.esta_vacio())

    def test_agregar_producto(self):
        self.carrito.agregar_producto(self.producto, 2)
        self.assertFalse(self.carrito.esta_vacio())
        self.assertEqual(self.carrito.cantidad_items(), 2)

    def test_calcular_subtotal(self):
        self.carrito.agregar_producto(self.producto, 3)
        self.assertAlmostEqual(self.carrito.calcular_subtotal(), 6000.0)

    def test_quitar_producto(self):
        self.carrito.agregar_producto(self.producto, 1)
        self.carrito.quitar_producto("Pantalon")
        self.assertTrue(self.carrito.esta_vacio())

    def test_quitar_producto_inexistente(self):
        with self.assertRaises(KeyError):
            self.carrito.quitar_producto("Inexistente")

    def test_agregar_cantidad_invalida(self):
        with self.assertRaises(ValueError):
            self.carrito.agregar_producto(self.producto, 0)

    def test_vaciar_carrito(self):
        self.carrito.agregar_producto(self.producto, 2)
        self.carrito.vaciar()
        self.assertTrue(self.carrito.esta_vacio())


# ─────────────────────────────────────────────
#  Componente: GestorDescuentos
# ─────────────────────────────────────────────
class TestGestorDescuentos(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorDescuentos()

    def test_sin_descuento(self):
        d = self.gestor.calcular_descuento(300.0, es_vip=False)
        self.assertEqual(d, 0.0)

    def test_descuento_monto_medio(self):
        d = self.gestor.calcular_descuento(600.0, es_vip=False)
        self.assertEqual(d, 0.03)

    def test_descuento_vip_sin_monto_alto(self):
        d = self.gestor.calcular_descuento(500.0, es_vip=True)
        self.assertEqual(d, 0.10)

    def test_descuento_vip_con_monto_alto(self):
        d = self.gestor.calcular_descuento(1500.0, es_vip=True)
        self.assertEqual(d, 0.15)

    def test_descuento_no_supera_limite(self):
        d = self.gestor.calcular_descuento(9999.0, es_vip=True)
        self.assertLessEqual(d, 0.15)

    def test_subtotal_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            self.gestor.calcular_descuento(-100.0, es_vip=False)

    def test_aplicar_descuento_resultado(self):
        resultado = self.gestor.aplicar_descuento(1000.0, es_vip=True)
        self.assertAlmostEqual(resultado, 900.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
