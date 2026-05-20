"""
SPRINT 2 — Prueba de Interfaz
Verifica los puntos de entrada públicos del sistema (la "interfaz" que el
usuario o un sistema externo usaría). Se prueba que los contratos de
entrada/salida sean correctos, completos y consistentes.
"""

import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.producto import Producto
from src.carrito import Carrito
from src.procesador_pedido import ProcesadorPedido


class TestInterfazProducto(unittest.TestCase):
    """Verifica la interfaz pública de la clase Producto."""

    def test_repr_es_string(self):
        p = Producto("Campera", 5000.0, 3)
        self.assertIsInstance(repr(p), str)
        self.assertIn("Campera", repr(p))

    def test_atributos_publicos_accesibles(self):
        p = Producto("Campera", 5000.0, 3)
        _ = p.nombre
        _ = p.precio
        _ = p.stock
        _ = p.tiene_stock()

    def test_metodo_reducir_stock_devuelve_none(self):
        p = Producto("Campera", 5000.0, 3)
        resultado = p.reducir_stock(1)
        self.assertIsNone(resultado)


class TestInterfazCarrito(unittest.TestCase):
    """Verifica la interfaz pública de la clase Carrito."""

    def setUp(self):
        self.carrito = Carrito()
        self.p = Producto("Remera", 800.0, 20)

    def test_agregar_devuelve_none(self):
        resultado = self.carrito.agregar_producto(self.p, 1)
        self.assertIsNone(resultado)

    def test_calcular_subtotal_devuelve_float(self):
        self.carrito.agregar_producto(self.p, 2)
        resultado = self.carrito.calcular_subtotal()
        self.assertIsInstance(resultado, float)

    def test_obtener_items_devuelve_dict(self):
        self.carrito.agregar_producto(self.p, 1)
        items = self.carrito.obtener_items()
        self.assertIsInstance(items, dict)
        self.assertIn("Remera", items)

    def test_repr_carrito(self):
        self.carrito.agregar_producto(self.p, 2)
        self.assertIsInstance(repr(self.carrito), str)
        self.assertIn("subtotal", repr(self.carrito))


class TestInterfazProcesadorPedido(unittest.TestCase):
    """Verifica que procesar() devuelva el contrato de datos correcto."""

    def setUp(self):
        self.procesador = ProcesadorPedido()
        self.carrito = Carrito()
        self.carrito.agregar_producto(Producto("Mochila", 1500.0, 5), 1)

    def test_resultado_contiene_claves_requeridas(self):
        claves_esperadas = {
            "subtotal", "porcentaje_descuento", "descuento_aplicado",
            "total_con_descuento", "tipo_envio", "costo_envio", "total_final"
        }
        resultado = self.procesador.procesar(self.carrito, False, "estandar")
        self.assertEqual(set(resultado.keys()), claves_esperadas)

    def test_resultado_tipos_correctos(self):
        resultado = self.procesador.procesar(self.carrito, False, "estandar")
        self.assertIsInstance(resultado["subtotal"], float)
        self.assertIsInstance(resultado["total_final"], float)
        self.assertIsInstance(resultado["tipo_envio"], str)
        self.assertIsInstance(resultado["costo_envio"], float)

    def test_total_final_mayor_o_igual_a_cero(self):
        resultado = self.procesador.procesar(self.carrito, False, "estandar")
        self.assertGreaterEqual(resultado["total_final"], 0.0)

    def test_tipo_envio_en_resultado_coincide_con_entrada(self):
        resultado = self.procesador.procesar(self.carrito, False, "express")
        self.assertEqual(resultado["tipo_envio"], "express")


if __name__ == "__main__":
    unittest.main(verbosity=2)
