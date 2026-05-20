"""
SPRINT 2 — Prueba de Rendimiento
Evalúa la velocidad de las operaciones críticas bajo carga repetida.
Se usa timeit para medir tiempos y se establecen umbrales máximos aceptables.
"""

import unittest
import timeit
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.producto import Producto
from src.carrito import Carrito
from src.gestor_descuentos import GestorDescuentos
from src.procesador_pedido import ProcesadorPedido


REPETICIONES = 10_000   # cantidad de ejecuciones por prueba
MAX_SEG_TOTAL = 2.0     # umbral máximo aceptable en segundos para N repeticiones


class TestRendimiento(unittest.TestCase):

    def test_rendimiento_calcular_subtotal(self):
        """calcular_subtotal() sobre carrito con 5 productos debe ser rápido."""
        carrito = Carrito()
        for i in range(5):
            carrito.agregar_producto(Producto(f"Prod{i}", float(i + 1) * 100, 50), 2)

        tiempo = timeit.timeit(
            lambda: carrito.calcular_subtotal(),
            number=REPETICIONES
        )
        print(f"\n  [Rendimiento] calcular_subtotal x{REPETICIONES}: {tiempo:.4f}s")
        self.assertLess(tiempo, MAX_SEG_TOTAL,
            f"calcular_subtotal tardó {tiempo:.4f}s para {REPETICIONES} llamadas (máx {MAX_SEG_TOTAL}s)")

    def test_rendimiento_calcular_descuento(self):
        """calcular_descuento() debe ejecutar 10.000 veces en menos de 2 segundos."""
        gestor = GestorDescuentos()

        tiempo = timeit.timeit(
            lambda: gestor.calcular_descuento(1500.0, True),
            number=REPETICIONES
        )
        print(f"\n  [Rendimiento] calcular_descuento x{REPETICIONES}: {tiempo:.4f}s")
        self.assertLess(tiempo, MAX_SEG_TOTAL)

    def test_rendimiento_procesar_pedido_completo(self):
        """El flujo completo de procesamiento debe mantenerse bajo umbral."""
        procesador = ProcesadorPedido()

        def flujo_completo():
            carrito = Carrito()
            p = Producto("Producto", 800.0, 100)
            carrito.agregar_producto(p, 3)
            procesador.procesar(carrito, es_vip=True, tipo_envio="estandar")

        tiempo = timeit.timeit(flujo_completo, number=1_000)
        print(f"\n  [Rendimiento] flujo completo x1000: {tiempo:.4f}s")
        self.assertLess(tiempo, MAX_SEG_TOTAL)

    def test_rendimiento_carrito_con_muchos_productos(self):
        """Agregar 100 productos distintos y calcular subtotal debe ser veloz."""
        def operacion():
            carrito = Carrito()
            for i in range(100):
                carrito.agregar_producto(Producto(f"P{i}", 10.0, 200), 1)
            carrito.calcular_subtotal()

        tiempo = timeit.timeit(operacion, number=100)
        print(f"\n  [Rendimiento] 100 productos x100 iteraciones: {tiempo:.4f}s")
        self.assertLess(tiempo, MAX_SEG_TOTAL)


if __name__ == "__main__":
    unittest.main(verbosity=2)
