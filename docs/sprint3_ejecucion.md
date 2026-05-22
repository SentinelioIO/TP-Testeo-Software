# Sprint 3 — Planificación, Ejecución y Documentación de Pruebas

## Plan de Ejecución

### Orden de ejecución definido

El orden sigue la pirámide de pruebas: primero las unidades base, luego integración, luego pruebas de mayor nivel.

| Orden | Suite                   | Razón                                        |
|-------|-------------------------|----------------------------------------------|
| 1°    | test_componentes.py     | Base: si las unidades fallan, todo falla      |
| 2°    | test_caja_negra.py      | Validar entradas/salidas sin dependencias     |
| 3°    | test_camino.py          | Cobertura de ramas antes de integrar          |
| 4°    | test_integracion.py     | Verificar comunicación entre clases           |
| 5°    | test_interfaz.py        | Validar contratos públicos del sistema        |
| 6°    | test_rendimiento.py     | Ejecutar último (requiere sistema estable)    |

### Comando de ejecución

```bash
python -m pytest tests/ -v --tb=short
```

### Datos de prueba utilizados

- Productos: precios entre $300 y $5000, stock entre 0 y 200 unidades
- Clientes: VIP y no VIP
- Tipos de envío: "estandar", "express", y casos inválidos
- Montos: valores bajo, en y sobre cada umbral ($500, $1000, $2000)

---

## Resultados de Ejecución

**Fecha de ejecución:** 22/05/2026  
**Entorno:** Python 3.12.3 | pytest 9.0.3 | Ubuntu 24  
**Comando ejecutado:** `python -m pytest tests/ -v --tb=short`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
collected 74 items

tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[300.0-False-300.0] PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[600.0-False-582.0] PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[500.0-True-450.0]  PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[1000.0-True-900.0] PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[1500.0-True-1275.0]PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[0.0-False-0.0]     PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[0.0-True-0.0]      PASSED
tests/test_caja_negra.py::test_aplicar_descuento_caja_negra[501.0-False-485.97]PASSED
tests/test_caja_negra.py::test_calcular_envio_caja_negra[500.0-estandar-500.0] PASSED
tests/test_caja_negra.py::test_calcular_envio_caja_negra[500.0-express-1000.0] PASSED
tests/test_caja_negra.py::test_calcular_envio_caja_negra[2000.0-estandar-0.0]  PASSED
tests/test_caja_negra.py::test_calcular_envio_caja_negra[2500.0-express-0.0]   PASSED
tests/test_caja_negra.py::test_calcular_envio_caja_negra[1999.99-estandar-500.0]PASSED
tests/test_caja_negra.py::test_reducir_stock_caja_negra[10-3-7-False]          PASSED
tests/test_caja_negra.py::test_reducir_stock_caja_negra[10-10-0-False]         PASSED
tests/test_caja_negra.py::test_reducir_stock_caja_negra[10-11-None-True]       PASSED
tests/test_caja_negra.py::test_reducir_stock_caja_negra[10-0-None-True]        PASSED
tests/test_caja_negra.py::test_reducir_stock_caja_negra[1-1-0-False]           PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C1_vip_monto_alto       PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C2_vip_monto_exacto_1000 PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C2_vip_monto_normal     PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C3_no_vip_monto_sobre_500 PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C4_borde_exacto_500     PASSED
tests/test_camino.py::TestCaminosGestorDescuentos::test_camino_C4_no_vip_monto_bajo_500 PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C5_borde_exacto_2000    PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C5_envio_gratis         PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C5_envio_gratis_sobre_umbral PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C6_envio_estandar       PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C7_envio_express        PASSED
tests/test_camino.py::TestCaminosProcesadorPedido::test_camino_C8_tipo_invalido        PASSED
tests/test_componentes.py::TestProducto::test_creacion_valida                  PASSED
tests/test_componentes.py::TestProducto::test_nombre_vacio_lanza_error         PASSED
tests/test_componentes.py::TestProducto::test_precio_negativo_lanza_error      PASSED
tests/test_componentes.py::TestProducto::test_reducir_stock_insuficiente       PASSED
tests/test_componentes.py::TestProducto::test_reducir_stock_valido             PASSED
tests/test_componentes.py::TestProducto::test_stock_negativo_lanza_error       PASSED
tests/test_componentes.py::TestProducto::test_tiene_stock_false                PASSED
tests/test_componentes.py::TestProducto::test_tiene_stock_true                 PASSED
tests/test_componentes.py::TestCarrito::test_agregar_cantidad_invalida         PASSED
tests/test_componentes.py::TestCarrito::test_agregar_producto                  PASSED
tests/test_componentes.py::TestCarrito::test_calcular_subtotal                 PASSED
tests/test_componentes.py::TestCarrito::test_carrito_inicia_vacio              PASSED
tests/test_componentes.py::TestCarrito::test_quitar_producto                   PASSED
tests/test_componentes.py::TestCarrito::test_quitar_producto_inexistente       PASSED
tests/test_componentes.py::TestCarrito::test_vaciar_carrito                    PASSED
tests/test_componentes.py::TestGestorDescuentos::test_aplicar_descuento_resultado PASSED
tests/test_componentes.py::TestGestorDescuentos::test_descuento_monto_medio    PASSED
tests/test_componentes.py::TestGestorDescuentos::test_descuento_no_supera_limite PASSED
tests/test_componentes.py::TestGestorDescuentos::test_descuento_vip_con_monto_alto PASSED
tests/test_componentes.py::TestGestorDescuentos::test_descuento_vip_sin_monto_alto PASSED
tests/test_componentes.py::TestGestorDescuentos::test_sin_descuento            PASSED
tests/test_componentes.py::TestGestorDescuentos::test_subtotal_negativo_lanza_error PASSED
tests/test_integracion.py::TestIntegracionCarritoDescuento::test_agregar_mismo_producto_dos_veces_acumula PASSED
tests/test_integracion.py::TestIntegracionCarritoDescuento::test_subtotal_con_multiples_productos_y_descuento_vip PASSED
tests/test_integracion.py::TestIntegracionCarritoDescuento::test_subtotal_sin_descuento_cliente_normal_bajo_500 PASSED
tests/test_integracion.py::TestIntegracionProcesadorPedido::test_carrito_vacio_lanza_error PASSED
tests/test_integracion.py::TestIntegracionProcesadorPedido::test_pedido_no_vip_con_envio_express PASSED
tests/test_integracion.py::TestIntegracionProcesadorPedido::test_pedido_vip_envio_gratis_por_monto PASSED
tests/test_integracion.py::TestIntegracionProcesadorPedido::test_tipo_envio_invalido_lanza_error PASSED
tests/test_interfaz.py::TestInterfazProducto::test_atributos_publicos_accesibles PASSED
tests/test_interfaz.py::TestInterfazProducto::test_metodo_reducir_stock_devuelve_none PASSED
tests/test_interfaz.py::TestInterfazProducto::test_repr_es_string              PASSED
tests/test_interfaz.py::TestInterfazCarrito::test_agregar_devuelve_none        PASSED
tests/test_interfaz.py::TestInterfazCarrito::test_calcular_subtotal_devuelve_float PASSED
tests/test_interfaz.py::TestInterfazCarrito::test_obtener_items_devuelve_dict  PASSED
tests/test_interfaz.py::TestInterfazCarrito::test_repr_carrito                 PASSED
tests/test_interfaz.py::TestInterfazProcesadorPedido::test_resultado_contiene_claves_requeridas PASSED
tests/test_interfaz.py::TestInterfazProcesadorPedido::test_resultado_tipos_correctos PASSED
tests/test_interfaz.py::TestInterfazProcesadorPedido::test_tipo_envio_en_resultado_coincide_con_entrada PASSED
tests/test_interfaz.py::TestInterfazProcesadorPedido::test_total_final_mayor_o_igual_a_cero PASSED
tests/test_rendimiento.py::TestRendimiento::test_rendimiento_calcular_descuento PASSED
tests/test_rendimiento.py::TestRendimiento::test_rendimiento_calcular_subtotal  PASSED
tests/test_rendimiento.py::TestRendimiento::test_rendimiento_carrito_con_muchos_productos PASSED
tests/test_rendimiento.py::TestRendimiento::test_rendimiento_procesar_pedido_completo PASSED

============================== 74 passed in 0.12s ==============================
```

---

## Resumen de Resultados

| Suite               | Pasaron | Fallaron | Total |
|---------------------|---------|----------|-------|
| Componentes         | 22      | 0        | 22    |
| Caja Negra          | 18      | 0        | 18    |
| Camino              | 12      | 0        | 12    |
| Integración         | 7       | 0        | 7     |
| Interfaz            | 11      | 0        | 11    |
| Rendimiento         | 4       | 0        | 4     |
| **TOTAL**           | **74**  | **0**    | **74**|

---

## Cobertura de Código

```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src/__init__.py                4      0   100%
src/carrito.py                30      2    93%   líneas 20, 22
src/gestor_descuentos.py      19      0   100%
src/procesador_pedido.py      24      0   100%
src/producto.py               21      0   100%
--------------------------------------------------------
TOTAL                         98      2    98%
```

**Cobertura total: 98%**

Las 2 líneas no cubiertas en `carrito.py` corresponden al manejo de un caso de sobrescritura de ítem ya existente en la versión anterior del dict, que fue refactorizado. No afectan la lógica de negocio activa.

---

## Defectos Encontrados

No se encontraron defectos durante la ejecución. Todos los casos de prueba pasaron en la primera ejecución, lo que valida la correctitud del diseño del sistema.

---

## Tiempo Total de Ejecución

**0.12 segundos** para 74 tests — cumple todos los requerimientos no funcionales de rendimiento.
