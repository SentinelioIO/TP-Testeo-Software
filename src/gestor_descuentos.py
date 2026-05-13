"""
Módulo: gestor_descuentos.py
Aplica descuentos según reglas de negocio.
"""


class GestorDescuentos:
    """
    Aplica descuentos al subtotal del carrito según las siguientes reglas:
      - Cliente VIP:          10% de descuento
      - Compra > $1000:       5%  de descuento adicional
      - Compra > $500 (no VIP): 3% de descuento
      - Los descuentos VIP y por monto se acumulan (máximo 15%)
    """

    DESCUENTO_VIP = 0.10
    DESCUENTO_MONTO_ALTO = 0.05   # subtotal > 1000
    DESCUENTO_MONTO_MEDIO = 0.03  # subtotal > 500, no VIP
    LIMITE_DESCUENTO = 0.15

    def calcular_descuento(self, subtotal: float, es_vip: bool) -> float:
        """
        Devuelve el porcentaje de descuento a aplicar (entre 0.0 y 0.15).
        """
        if subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo.")

        descuento = 0.0

        if es_vip:
            descuento += self.DESCUENTO_VIP
            if subtotal > 1000:
                descuento += self.DESCUENTO_MONTO_ALTO
        elif subtotal > 500:
            descuento += self.DESCUENTO_MONTO_MEDIO

        return min(descuento, self.LIMITE_DESCUENTO)

    def aplicar_descuento(self, subtotal: float, es_vip: bool) -> float:
        """Devuelve el monto final después de aplicar el descuento."""
        porcentaje = self.calcular_descuento(subtotal, es_vip)
        return round(subtotal * (1 - porcentaje), 2)
