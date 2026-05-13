"""
Módulo: procesador_pedido.py
Orquesta el flujo completo de compra: carrito → descuento → envío → total.
"""

from src.carrito import Carrito
from src.gestor_descuentos import GestorDescuentos


COSTO_ENVIO_ESTANDAR = 500.0
COSTO_ENVIO_EXPRESS  = 1000.0
ENVIO_GRATIS_DESDE   = 2000.0


class ProcesadorPedido:
    """
    Procesa el pedido final: aplica descuentos, calcula envío y genera resumen.
    Tipos de envío aceptados: 'estandar', 'express'
    """

    TIPOS_ENVIO = {"estandar": COSTO_ENVIO_ESTANDAR, "express": COSTO_ENVIO_EXPRESS}

    def __init__(self):
        self.gestor = GestorDescuentos()

    def calcular_envio(self, subtotal_con_descuento: float, tipo_envio: str) -> float:
        """Calcula el costo de envío. Gratis si el total supera ENVIO_GRATIS_DESDE."""
        if tipo_envio not in self.TIPOS_ENVIO:
            raise ValueError(
                f"Tipo de envío '{tipo_envio}' no válido. "
                f"Opciones: {list(self.TIPOS_ENVIO.keys())}"
            )
        if subtotal_con_descuento >= ENVIO_GRATIS_DESDE:
            return 0.0
        return self.TIPOS_ENVIO[tipo_envio]

    def procesar(self, carrito: Carrito, es_vip: bool, tipo_envio: str) -> dict:
        """
        Procesa el pedido completo.
        Retorna un dict con subtotal, descuento, envio y total.
        """
        if carrito.esta_vacio():
            raise ValueError("No se puede procesar un carrito vacío.")

        subtotal = carrito.calcular_subtotal()
        porcentaje_descuento = self.gestor.calcular_descuento(subtotal, es_vip)
        total_con_descuento = self.gestor.aplicar_descuento(subtotal, es_vip)
        costo_envio = self.calcular_envio(total_con_descuento, tipo_envio)
        total_final = round(total_con_descuento + costo_envio, 2)

        return {
            "subtotal": subtotal,
            "porcentaje_descuento": porcentaje_descuento,
            "descuento_aplicado": round(subtotal - total_con_descuento, 2),
            "total_con_descuento": total_con_descuento,
            "tipo_envio": tipo_envio,
            "costo_envio": costo_envio,
            "total_final": total_final,
        }
