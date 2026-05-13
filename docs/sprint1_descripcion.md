# Sprint 1 — Descripción del Software

## Objetivo del Software

**Sistema de Carrito de Compras** es una aplicación de consola orientada a objetos desarrollada en Python que simula el flujo de compra de un e-commerce. Permite gestionar productos, armar un carrito, aplicar descuentos según perfil del cliente y calcular el total final con costo de envío.

---

## Requerimientos Implementados

### Funcionales

| ID  | Requerimiento |
|-----|---------------|
| RF1 | El sistema permite crear productos con nombre, precio y stock. |
| RF2 | El sistema permite agregar y quitar productos del carrito. |
| RF3 | El sistema calcula el subtotal del carrito en cualquier momento. |
| RF4 | El sistema aplica descuentos según si el cliente es VIP y el monto total. |
| RF5 | El sistema calcula el costo de envío (estándar o express) con envío gratis para compras mayores a $2000 post-descuento. |
| RF6 | El sistema procesa un pedido completo y devuelve un resumen detallado. |

### No Funcionales

| ID   | Requerimiento |
|------|---------------|
| RNF1 | El sistema debe calcular 10.000 descuentos en menos de 2 segundos. |
| RNF2 | El sistema debe manejar excepciones con mensajes claros ante entradas inválidas. |
| RNF3 | Cobertura de código mayor al 95% medida con pytest-cov. |
| RNF4 | El código debe seguir principios OOP: encapsulamiento, responsabilidad única. |

---

## Clases del Sistema

| Clase               | Responsabilidad |
|---------------------|-----------------|
| `Producto`          | Representa un artículo del catálogo con precio y stock. |
| `Carrito`           | Gestiona los ítems seleccionados por el usuario. |
| `GestorDescuentos`  | Aplica reglas de negocio para calcular descuentos. |
| `ProcesadorPedido`  | Orquesta el flujo completo: descuento + envío + total. |

---

## Reglas de Negocio

- Cliente VIP: 10% de descuento
- Compra mayor a $1000 + VIP: 5% adicional (total 15%)
- Compra mayor a $500 sin VIP: 3% de descuento
- Envío gratis para totales post-descuento ≥ $2000
- Envío estándar: $500 | Envío express: $1000

---

## Código Fuente

Disponible en: `src/`
- `src/producto.py`
- `src/carrito.py`
- `src/gestor_descuentos.py`
- `src/procesador_pedido.py`

---

## Artefactos UML

### Diagrama de Clases

```
┌──────────────────────────────┐
│         Producto             │
├──────────────────────────────┤
│ + nombre: str                │
│ + precio: float              │
│ + stock: int                 │
├──────────────────────────────┤
│ + tiene_stock(): bool        │
│ + reducir_stock(cant: int)   │
└──────────────────────────────┘
          ◇ (usa)
          │
┌──────────────────────────────┐
│          Carrito             │
├──────────────────────────────┤
│ - _items: dict               │
├──────────────────────────────┤
│ + agregar_producto(p, cant)  │
│ + quitar_producto(nombre)    │
│ + calcular_subtotal(): float │
│ + cantidad_items(): int      │
│ + esta_vacio(): bool         │
│ + vaciar()                   │
└──────────────────────────────┘
          ◇ (usa)
          │
┌──────────────────────────────┐        ┌───────────────────────────────┐
│      ProcesadorPedido        │───────>│      GestorDescuentos         │
├──────────────────────────────┤        ├───────────────────────────────┤
│ - gestor: GestorDescuentos   │        │ DESCUENTO_VIP = 0.10          │
├──────────────────────────────┤        │ DESCUENTO_MONTO_ALTO = 0.05   │
│ + calcular_envio(t, tipo)    │        │ DESCUENTO_MONTO_MEDIO = 0.03  │
│ + procesar(carrito, vip, env)│        ├───────────────────────────────┤
└──────────────────────────────┘        │ + calcular_descuento(): float │
                                        │ + aplicar_descuento(): float  │
                                        └───────────────────────────────┘
```

### Diagrama de Casos de Uso

```
         ┌─────────────────────────────────────────┐
         │          Sistema de Compras             │
         │                                         │
  [User] ─── Agregar producto al carrito           │
  [User] ─── Ver subtotal del carrito              │
  [User] ─── Quitar producto del carrito           │
  [User] ─── Vaciar carrito                        │
  [User] ─── Procesar pedido (con tipo de envío)   │
         │         │                               │
         │    <<include>>                          │
         │    Aplicar descuento (VIP/monto)        │
         │    Calcular costo de envío              │
         └─────────────────────────────────────────┘
```

---

## Link al Repositorio

https://github.com/SentinelioIO/TP-Testeo-Software
