# TP Final — Testeo de Software
**Universidad de Belgrano | Facultad de Ingeniería y Tecnología Informática**  
Técnico en Programación de Computadoras — 2026  
Profesor: Octavio Villegas

---

## Sistema bajo prueba: Carrito de Compras

Aplicación orientada a objetos en Python que simula el flujo de compra de un e-commerce.  
**4 clases** | **74 tests** | **98% de cobertura**

---

## Estructura del Proyecto

```
TP-Testeo-Software/
├── src/
│   ├── producto.py           # Clase Producto
│   ├── carrito.py            # Clase Carrito
│   ├── gestor_descuentos.py  # Clase GestorDescuentos
│   └── procesador_pedido.py  # Clase ProcesadorPedido
├── tests/
│   ├── test_componentes.py   # Sprint 2.1
│   ├── test_integracion.py   # Sprint 2.2
│   ├── test_caja_negra.py    # Sprint 2.3
│   ├── test_rendimiento.py   # Sprint 2.4
│   ├── test_interfaz.py      # Sprint 2.5
│   └── test_camino.py        # Sprint 2.6
└── docs/
    ├── sprint1_descripcion.md
    ├── sprint2_conjunto_pruebas.md
    ├── sprint3_ejecucion.md
    └── sprint4_e2e.md
```

---

## Cómo ejecutar

```bash
# Instalar dependencias
pip install pytest pytest-cov

# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar con reporte de cobertura
python -m pytest tests/ --cov=src --cov-report=term-missing
```

---

## Sprints

| Sprint | Fecha | Contenido | Estado |
|--------|-------|-----------|--------|
| 1      | 13/05 | Software + UML + Descripción | ✅ |
| 2      | 20/05 | Diseño del conjunto de pruebas | ✅ |
| 3      | 27/05 | Ejecución y documentación | ✅ |
| 4      | 03/06 | Pruebas E2E | 🔄 |
| Final  | 10/06 | Entrega completa | 🔄 |
