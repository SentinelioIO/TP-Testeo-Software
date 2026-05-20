"""
SPRINT 2 — Prueba de Camino (Path Testing)
Técnica de caja blanca: se diseña un caso de prueba por cada camino
lógico posible dentro de las funciones. Cubre todas las ramas if/elif/else.

Función analizada: GestorDescuentos.calcular_descuento(subtotal, es_vip)
Función analizada: ProcesadorPedido.calcular_envio(total, tipo_envio)

Caminos en calcular_descuento:
  C1: es_vip=True  AND subtotal > 1000   → descuento = 0.10 + 0.05 = 0.15
  C2: es_vip=True  AND subtotal <= 1000  → descuento = 0.10
  C3: es_vip=False AND subtotal > 500    → descuento = 0.03
  C4: es_vip=False AND subtotal <= 500   → descuento = 0.0

Caminos en calcular_envio:
  C5: total >= ENVIO_GRATIS_DESDE        → costo = 0.0
  C6: total <  ENVIO_GRATIS_DESDE, tipo "estandar" → 500
  C7: total <  ENVIO_GRATIS_DESDE, tipo "express"  → 1000
  C8: tipo inválido                      → ValueError
"""

import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.gestor_descuentos import GestorDescuentos
from src.procesador_pedido import ProcesadorPedido


class TestCaminosGestorDescuentos(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorDescuentos()

    def test_camino_C1_vip_monto_alto(self):
        """C1: VIP + monto > 1000 → 15% descuento acumulado."""
        descuento = self.gestor.calcular_descuento(1500.0, es_vip=True)
        self.assertEqual(descuento, 0.15)

    def test_camino_C2_vip_monto_normal(self):
        """C2: VIP + monto <= 1000 → solo 10%."""
        descuento = self.gestor.calcular_descuento(999.0, es_vip=True)
        self.assertEqual(descuento, 0.10)

    def test_camino_C2_vip_monto_exacto_1000(self):
        """C2 borde: VIP con exactamente 1000 → solo 10% (no entra al if > 1000)."""
        descuento = self.gestor.calcular_descuento(1000.0, es_vip=True)
        self.assertEqual(descuento, 0.10)

    def test_camino_C3_no_vip_monto_sobre_500(self):
        """C3: No VIP + monto > 500 → 3%."""
        descuento = self.gestor.calcular_descuento(501.0, es_vip=False)
        self.assertEqual(descuento, 0.03)

    def test_camino_C4_no_vip_monto_bajo_500(self):
        """C4: No VIP + monto <= 500 → sin descuento."""
        descuento = self.gestor.calcular_descuento(400.0, es_vip=False)
        self.assertEqual(descuento, 0.0)

    def test_camino_C4_borde_exacto_500(self):
        """C4 borde: monto exactamente 500 → sin descuento (no supera 500)."""
        descuento = self.gestor.calcular_descuento(500.0, es_vip=False)
        self.assertEqual(descuento, 0.0)


class TestCaminosProcesadorPedido(unittest.TestCase):

    def setUp(self):
        self.procesador = ProcesadorPedido()

    def test_camino_C5_envio_gratis(self):
        """C5: total >= 2000 → envío gratis."""
        costo = self.procesador.calcular_envio(2000.0, "estandar")
        self.assertEqual(costo, 0.0)

    def test_camino_C5_envio_gratis_sobre_umbral(self):
        """C5: total > 2000 con express → sigue siendo gratis."""
        costo = self.procesador.calcular_envio(3000.0, "express")
        self.assertEqual(costo, 0.0)

    def test_camino_C6_envio_estandar(self):
        """C6: total < 2000, tipo estandar → $500."""
        costo = self.procesador.calcular_envio(1999.0, "estandar")
        self.assertEqual(costo, 500.0)

    def test_camino_C7_envio_express(self):
        """C7: total < 2000, tipo express → $1000."""
        costo = self.procesador.calcular_envio(500.0, "express")
        self.assertEqual(costo, 1000.0)

    def test_camino_C8_tipo_invalido(self):
        """C8: tipo de envío inválido → ValueError."""
        with self.assertRaises(ValueError):
            self.procesador.calcular_envio(500.0, "drone")

    def test_camino_C5_borde_exacto_2000(self):
        """C5 borde: exactamente 2000 → gratis (es >=)."""
        costo = self.procesador.calcular_envio(2000.0, "express")
        self.assertEqual(costo, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
