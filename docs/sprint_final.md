# Sprint Final — Introduccion de Error de Logica

## Objetivo

Demostrar el valor de una suite de tests completa introduciendo un error real en el codigo y observando como los tests lo detectan automaticamente en distintas capas del sistema.

---

## El Error Introducido

Archivo: src/gestor_descuentos.py
Tipo de error: Error de logica en condicion de borde

Cambio realizado:

    # ANTES (correcto)
    if subtotal > 1000:
        descuento += self.DESCUENTO_MONTO_ALTO

    # DESPUES (con error)
    if subtotal >= 1000:
        descuento += self.DESCUENTO_MONTO_ALTO

La regla de negocio establece que el descuento adicional del 5% se aplica cuando el subtotal es mayor a $1000. Con el cambio a >=, el descuento extra tambien se aplica cuando el subtotal es exactamente $1000, lo cual es incorrecto.

Un cliente VIP con subtotal de $1000 deberia recibir 10% de descuento (total $900), pero con el error recibe 15% (total $850).

---

## Impacto en los Tests

El error afecto 3 tests en 3 archivos distintos:

| Test | Archivo | Error detectado |
|------|---------|-----------------|
| test_aplicar_descuento_resultado | test_componentes.py | Esperaba $900, obtuvo $850 |
| test_aplicar_descuento_caja_negra[1000.0-True-900.0] | test_caja_negra.py | Esperaba $900, obtuvo $850 |
| test_camino_C2_vip_monto_exacto_1000 | test_camino.py | Esperaba descuento 0.10, obtuvo 0.15 |

---

## Resultado de Ejecucion

Comando:

    python -m pytest tests/ -v

Resultado:

    FAILED tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[1000.0-True-900.0]
    FAILED tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C2_vip_monto_exacto_1000
    FAILED tests/test_componentes.py::TestGestorDescuentos::test_aplicar_descuento_resultado

    3 failed, 78 passed in 0.23s

---

## Conclusion

Un solo cambio en una condicion de borde (> por >=) fue suficiente para romper tests en tres archivos distintos: prueba de componentes, caja negra y camino. Esto demuestra el valor de tener cobertura en multiples capas: el error no se escapo porque estaba cubierto desde distintos angulos.