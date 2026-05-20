"""
SPRINT 2 — Prueba de Caja Negra
Se prueba la funcionalidad desde fuera: solo entradas y salidas esperadas,
sin conocimiento del código interno. Se usa pytest con parametrize.
"""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.gestor_descuentos import GestorDescuentos
from src.procesador_pedido import ProcesadorPedido
from src.carrito import Carrito
from src.producto import Producto


gestor = GestorDescuentos()


# ─────────────────────────────────────────────
#  Caja Negra: GestorDescuentos
#  Entrada: (subtotal, es_vip) → Salida: total esperado
# ─────────────────────────────────────────────
@pytest.mark.parametrize("subtotal, es_vip, total_esperado", [
    (300.0,   False, 300.0),    # Sin descuento
    (600.0,   False, 582.0),    # 3% descuento por monto medio
    (500.0,   True,  450.0),    # VIP 10%
    (1000.0,  True,  900.0),    # VIP 10%
    (1500.0,  True,  1275.0),   # VIP + monto alto = 15%
    (0.0,     False, 0.0),      # Carrito en cero
    (0.0,     True,  0.0),      # VIP con carrito en cero
    (501.0,   False, 485.97),   # Justo sobre el límite de 500
])
def test_aplicar_descuento_caja_negra(subtotal, es_vip, total_esperado):
    resultado = gestor.aplicar_descuento(subtotal, es_vip)
    assert abs(resultado - total_esperado) < 0.01, (
        f"subtotal={subtotal}, vip={es_vip} → esperado {total_esperado}, obtenido {resultado}"
    )


# ─────────────────────────────────────────────
#  Caja Negra: ProcesadorPedido.calcular_envio
#  Entrada: (total_con_descuento, tipo_envio) → costo_envio esperado
# ─────────────────────────────────────────────
procesador = ProcesadorPedido()

@pytest.mark.parametrize("total, tipo_envio, envio_esperado", [
    (500.0,   "estandar", 500.0),   # Bajo el umbral, envío estándar
    (500.0,   "express",  1000.0),  # Bajo el umbral, envío express
    (2000.0,  "estandar", 0.0),     # Exactamente en el umbral → gratis
    (2500.0,  "express",  0.0),     # Sobre el umbral → gratis
    (1999.99, "estandar", 500.0),   # Justo bajo el umbral
])
def test_calcular_envio_caja_negra(total, tipo_envio, envio_esperado):
    resultado = procesador.calcular_envio(total, tipo_envio)
    assert resultado == envio_esperado


# ─────────────────────────────────────────────
#  Caja Negra: Producto.reducir_stock
# ─────────────────────────────────────────────
@pytest.mark.parametrize("stock_inicial, cantidad, stock_esperado, debe_fallar", [
    (10, 3,  7,    False),
    (10, 10, 0,    False),
    (10, 11, None, True),   # stock insuficiente
    (10, 0,  None, True),   # cantidad inválida
    (1,  1,  0,    False),
])
def test_reducir_stock_caja_negra(stock_inicial, cantidad, stock_esperado, debe_fallar):
    from src.producto import Producto
    p = Producto("Test", 100.0, stock_inicial)
    if debe_fallar:
        with pytest.raises(ValueError):
            p.reducir_stock(cantidad)
    else:
        p.reducir_stock(cantidad)
        assert p.stock == stock_esperado
