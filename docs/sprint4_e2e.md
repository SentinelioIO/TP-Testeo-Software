# Sprint 4 — Pruebas End-to-End (E2E)

## ¿Qué es una prueba E2E?

Una prueba E2E valida el flujo completo de la aplicación desde la perspectiva del usuario final, atravesando todas las capas del sistema de punta a punta. A diferencia de las pruebas de componentes o integración, no se testea una clase sola ni la interacción entre dos módulos — se simula un escenario real completo.

---

## Sistema bajo prueba

Carrito de compras en Python. El flujo completo involucra las 4 clases:

Producto → Carrito → GestorDescuentos → ProcesadorPedido

---

## Escenarios E2E diseñados

| ID | Escenario | Cliente | Envío | Resultado esperado |
|----|-----------|---------|-------|-------------------|
| E2E-01 | Compra simple | No VIP | Estándar | Descuento 3%, total $1276 |
| E2E-02 | Compra VIP con descuento máximo | VIP | Estándar | Descuento 15%, total $2285 |
| E2E-03 | Envío gratis por monto alto | No VIP | Estándar | Envío $0, total $2910 |
| E2E-04 | Envío express | No VIP | Express | Envío $1000, total $1533.5 |
| E2E-05 | Carrito vacío | — | — | ValueError |
| E2E-06 | Stock insuficiente | — | — | ValueError |
| E2E-07 | Quitar producto y procesar | No VIP | Estándar | Solo queda 1 producto, total $1373 |

---

## Ejecución

Comando utilizado:

    python -m pytest tests/test_e2e.py -v

### Resultado

    collected 7 items

    tests/test_e2e.py::TestE2EFlujoBasico::test_compra_simple_cliente_normal PASSED
    tests/test_e2e.py::TestE2EFlujoVIP::test_compra_vip_descuento_maximo PASSED
    tests/test_e2e.py::TestE2EFlujoEnvioGratis::test_envio_gratis_subtotal_alto PASSED
    tests/test_e2e.py::TestE2EFlujoExpress::test_compra_con_envio_express PASSED
    tests/test_e2e.py::TestE2EFlujoCarritoVacio::test_error_carrito_vacio PASSED
    tests/test_e2e.py::TestE2EFlujoStockInsuficiente::test_error_stock_insuficiente PASSED
    tests/test_e2e.py::TestE2EFlujoQuitarProducto::test_quitar_producto_y_procesar PASSED

    7 passed in 0.04s

---

## Observaciones

- El descuento se aplica sobre el subtotal antes de calcular si el envío es gratis.
- Un cliente VIP con subtotal $2100 obtiene 15% de descuento, lo que da $1785, que no supera el umbral de $2000 para envío gratis.
- Los flujos de error (carrito vacío, stock insuficiente) también se validan como parte del E2E.