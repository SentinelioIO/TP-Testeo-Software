# Sprint 2 — Diseño del Conjunto de Pruebas

## Resumen

| Tipo de Prueba       | Archivo                    | Casos | Herramienta |
|----------------------|----------------------------|-------|-------------|
| Componentes          | test_componentes.py        | 22    | unittest    |
| Integración          | test_integracion.py        | 7     | unittest    |
| Caja Negra           | test_caja_negra.py         | 18    | pytest      |
| Rendimiento          | test_rendimiento.py        | 4     | timeit      |
| Interfaz             | test_interfaz.py           | 11    | unittest    |
| Camino               | test_camino.py             | 12    | unittest    |
| **TOTAL**            |                            | **74**|             |

---

## 2.1 Prueba de Componentes

**Definición:** Se prueba cada clase de forma aislada, sin depender de otras clases del sistema.

**Clases probadas:** `Producto`, `Carrito`, `GestorDescuentos`

**Casos de prueba seleccionados:**

| ID  | Clase             | Caso                                     | Resultado esperado        |
|-----|-------------------|------------------------------------------|---------------------------|
| C01 | Producto          | Creación con datos válidos               | Objeto creado correctamente|
| C02 | Producto          | tiene_stock() con stock > 0             | True                       |
| C03 | Producto          | tiene_stock() con stock = 0             | False                      |
| C04 | Producto          | reducir_stock() válido                  | Stock decrementado         |
| C05 | Producto          | reducir_stock() mayor al stock          | ValueError                 |
| C06 | Producto          | Precio negativo                         | ValueError                 |
| C07 | Producto          | Nombre vacío                            | ValueError                 |
| C08 | Producto          | Stock negativo                          | ValueError                 |
| C09 | Carrito           | Carrito inicia vacío                    | esta_vacio() = True        |
| C10 | Carrito           | Agregar producto                        | cantidad_items() > 0       |
| C11 | Carrito           | calcular_subtotal() correcto            | precio × cantidad          |
| C12 | Carrito           | Quitar producto existente               | Carrito vacío              |
| C13 | Carrito           | Quitar producto inexistente             | KeyError                   |
| C14 | Carrito           | Cantidad inválida al agregar            | ValueError                 |
| C15 | Carrito           | Vaciar carrito                          | esta_vacio() = True        |
| C16 | GestorDescuentos  | Sin descuento (monto bajo, no VIP)      | 0.0                        |
| C17 | GestorDescuentos  | Descuento por monto medio               | 0.03                       |
| C18 | GestorDescuentos  | Descuento VIP sin monto alto            | 0.10                       |
| C19 | GestorDescuentos  | Descuento VIP con monto alto            | 0.15                       |
| C20 | GestorDescuentos  | Descuento no supera límite 15%          | ≤ 0.15                     |
| C21 | GestorDescuentos  | Subtotal negativo                       | ValueError                 |
| C22 | GestorDescuentos  | aplicar_descuento() resultado correcto  | Monto reducido             |

---

## 2.2 Prueba de Integración

**Definición:** Se verifica que las clases interactúen correctamente entre sí.

**Flujos probados:**
- `Carrito` + `GestorDescuentos`
- `Carrito` + `ProcesadorPedido` (que internamente usa `GestorDescuentos`)

| ID  | Flujo                                    | Resultado esperado            |
|-----|------------------------------------------|-------------------------------|
| I01 | Multi-producto + descuento VIP 15%       | Total = subtotal × 0.85       |
| I02 | Cliente normal bajo $500, sin descuento  | Total = subtotal sin cambios  |
| I03 | Mismo producto agregado dos veces        | Cantidades acumuladas         |
| I04 | VIP con compra > $2000 → envío gratis    | costo_envio = 0               |
| I05 | No VIP + envío express                   | costo_envio = 1000            |
| I06 | Carrito vacío al procesar               | ValueError                    |
| I07 | Tipo de envío inválido                   | ValueError                    |

---

## 2.3 Prueba de Caja Negra

**Definición:** Solo se conocen las entradas y salidas esperadas; no se inspecciona el código interno.

**Técnica:** `@pytest.mark.parametrize` — permite cubrir múltiples combinaciones de entrada en un solo test.

**Tabla de datos de prueba — `aplicar_descuento(subtotal, es_vip)`:**

| subtotal | es_vip | total_esperado | Razón                          |
|----------|--------|----------------|--------------------------------|
| 300.0    | False  | 300.0          | Sin descuento                  |
| 600.0    | False  | 582.0          | 3% descuento monto medio       |
| 500.0    | True   | 450.0          | VIP 10%                        |
| 1000.0   | True   | 900.0          | VIP 10%                        |
| 1500.0   | True   | 1275.0         | VIP + monto alto = 15%         |
| 0.0      | False  | 0.0            | Carrito vacío                  |
| 501.0    | False  | 485.97         | Justo sobre el límite de $500  |

---

## 2.4 Prueba de Rendimiento

**Definición:** Se mide el tiempo de ejecución bajo carga repetida y se valida contra umbrales.

**Umbrales definidos:** 10.000 repeticiones en menos de 2 segundos.

| Operación                   | Repeticiones | Umbral máx. |
|-----------------------------|--------------|-------------|
| calcular_subtotal()         | 10.000       | 2 seg       |
| calcular_descuento()        | 10.000       | 2 seg       |
| Flujo completo procesar()   | 1.000        | 2 seg       |
| Carrito con 100 productos   | 100          | 2 seg       |

---

## 2.5 Prueba de Interfaz

**Definición:** Se verifican los contratos de la interfaz pública de cada clase: tipos de retorno, claves del dict de respuesta, formato del repr.

| Elemento probado                          | Verificación                              |
|-------------------------------------------|-------------------------------------------|
| `Producto.__repr__`                       | Devuelve string que contiene el nombre    |
| `Carrito.calcular_subtotal()`             | Devuelve float                            |
| `Carrito.obtener_items()`                 | Devuelve dict con nombre como clave       |
| `ProcesadorPedido.procesar()` — claves    | 7 claves requeridas presentes             |
| `ProcesadorPedido.procesar()` — tipos     | subtotal float, tipo_envio str            |
| `ProcesadorPedido.procesar()` — invariante| total_final ≥ 0                           |

---

## 2.6 Prueba de Camino

**Definición:** Técnica de caja blanca — se crea un caso de prueba por cada rama lógica posible.

**Función analizada: `calcular_descuento(subtotal, es_vip)`**

```
C1: es_vip=True  AND subtotal > 1000   → 0.15
C2: es_vip=True  AND subtotal <= 1000  → 0.10
C3: es_vip=False AND subtotal > 500    → 0.03
C4: es_vip=False AND subtotal <= 500   → 0.00
```

**Función analizada: `calcular_envio(total, tipo_envio)`**

```
C5: total >= 2000                        → 0.00 (gratis)
C6: total < 2000, tipo = "estandar"      → 500.0
C7: total < 2000, tipo = "express"       → 1000.0
C8: tipo inválido                        → ValueError
```

Además se agregaron casos borde (valores exactos en los límites de cada condición).
