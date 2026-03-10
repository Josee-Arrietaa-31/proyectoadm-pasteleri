# Sprint 2 — Tareas Pendientes (antes de la próxima clase)
**Fecha límite estimada:** próxima clase  
**Proyecto:** Implementación de Odoo — Pastelería/Panadería

---

## Resumen de entregables requeridos por el profesor

| # | Tarea | Responsable | Estado |
|---|-------|-------------|--------|
| 1 | Instalar Odoo | — | ⬜ Pendiente |
| 2 | Crear catálogo de productos (pastelería/panadería) | — | ⬜ Pendiente |
| 3 | Registrar cantidades iniciales en Inventario | — | ⬜ Pendiente |
| 4 | Simular una venta sencilla (cliente + producto) | — | ⬜ Pendiente |
| 5 | Llevar el roadmap del proyecto para revisión | — | ✅ Ya está en documento Word del Sprint 1 |

---

## Tarea 1 — Instalación de Odoo

### Opción recomendada: Odoo Community (gratuita)

1. Ir a [https://www.odoo.com/es/download](https://www.odoo.com/es/download)
2. Descargar el instalador para Windows.
3. Seguir el asistente de instalación:
   - Se instala también PostgreSQL automáticamente.
   - Crear una base de datos nueva (ej. `pasteleria_db`).
   - Idioma: Español.
4. Acceder desde el navegador en: `http://localhost:8069`
5. Activar los módulos necesarios:
   - **Inventario** (`Inventory`)
   - **Ventas** (`Sales`)
   - **Punto de Venta** (`Point of Sale`) — opcional para demo de ventas
   - **Facturación** (`Invoicing`) — opcional

> **Alternativa rápida:** Usar [Odoo Online (prueba gratuita 15 días)](https://www.odoo.com/es/trial) si no quieren instalar nada localmente.

---

## Tarea 2 — Catálogo de Productos (Pastelería/Panadería)

### Dónde configurarlo en Odoo
`Inventario > Productos > Productos > Nuevo`  
o  
`Ventas > Productos > Productos > Nuevo`

### Productos sugeridos para el catálogo

| Nombre del Producto | Categoría | Precio Venta | Unidad de Medida | ¿Se vende? | ¿Se compra? |
|---------------------|-----------|-------------|------------------|-----------|------------|
| Pastel de Chocolate | Pasteles | ₡8,500 | Unidad | ✔ | — |
| Pastel de Vainilla | Pasteles | ₡7,500 | Unidad | ✔ | — |
| Pastel de Tres Leches | Pasteles | ✔ | ₡9,000 | Unidad | — |
| Pan de Mantequilla (unidad) | Pan | ₡350 | Unidad | ✔ | — |
| Pan Integral (barra) | Pan | ₡1,200 | Unidad | ✔ | — |
| Galletas con Chispas (bolsa) | Repostería | ₡1,800 | Bolsa | ✔ | — |
| Muffin de Arándanos | Repostería | ₡900 | Unidad | ✔ | — |
| Croissant | Pan | ₡750 | Unidad | ✔ | — |
| Cupcake Decorado | Repostería | ₡1,200 | Unidad | ✔ | — |
| Brownie de Chocolate | Repostería | ₡850 | Unidad | ✔ | — |

### Pasos para crear un producto
1. Ir a **Inventario > Productos > Nuevo**.
2. Ingresar nombre del producto.
3. Asignar **Categoría interna** (ej. "Pasteles", "Pan", "Repostería").
4. Definir precio de venta.
5. En la pestaña **"General"**: activar **"Puede ser vendido"** y **"Puede ser comprado"** según aplique.
6. En la pestaña **"Inventario"**: definir la ruta de almacenamiento (ej. "Almacenar").
7. **Guardar**.

> **Tip:** Crear primero las categorías de producto en `Inventario > Configuración > Categorías de Producto` para tenerlas disponibles.

---

## Tarea 3 — Inventario (Cantidades Iniciales y Movimientos)

### Registrar cantidades iniciales
`Inventario > Operaciones > Ajustes de Inventario`

1. Abrir **Ajustes de Inventario**.
2. Hacer clic en **"Crear"** o seleccionar los productos existentes.
3. Para cada producto, ingresar la cantidad disponible actual.
4. Clic en **"Aplicar todos"** para confirmar.

### Cantidades iniciales sugeridas para la demo

| Producto | Cantidad Inicial |
|----------|-----------------|
| Pastel de Chocolate | 5 |
| Pastel de Vainilla | 5 |
| Pan de Mantequilla | 30 |
| Pan Integral | 10 |
| Galletas con Chispas | 20 |
| Muffin de Arándanos | 15 |
| Croissant | 25 |
| Cupcake Decorado | 12 |
| Brownie de Chocolate | 18 |

### Registrar un movimiento básico (recepción de mercancía)
`Inventario > Operaciones > Recepciones > Crear`

1. Crear nuevo recibo de bodega.
2. Agregar los productos con las cantidades.
3. Validar la operación → el inventario se actualiza automáticamente.

---

## Tarea 4 — Demo de Ventas (Registrar Cliente y Simular Venta)

### Paso A: Registrar un cliente
`Ventas > Pedidos > Clientes > Crear`

Datos sugeridos para el cliente demo:
- **Nombre:** Laura Rodríguez
- **Tipo:** Persona
- **Correo:** laura.rodriguez@ejemplo.com
- **Teléfono:** 8888-0000
- **País:** Costa Rica

### Paso B: Crear una orden de venta
`Ventas > Pedidos > Pedidos > Crear`

1. Seleccionar el cliente **"Laura Rodríguez"**.
2. Agregar líneas de producto:
   - 1 × Pastel de Chocolate — ₡8,500
   - 2 × Croissant — ₡750 c/u
3. **Confirmar el pedido**.
4. Notar cómo el sistema genera automáticamente órdenes de entrega en Inventario.

### Paso C: Validar la entrega (afecta inventario)
`Inventario > Operaciones > Transferencias`

1. Localizar la transferencia generada.
2. Revisar que los productos y cantidades coincidan.
3. Hacer clic en **"Validar"**.
4. Verificar que el inventario se redujo correctamente.

### Paso D: Facturar la venta (opcional para la demo)
`Ventas > Pedidos > Pedidos > [Pedido] > Crear Factura > Confirmar`

---

## Relación entre módulos (cómo explicárselo al profe)

```
[Catálogo de Productos]
        ↓
[Inventario: Cantidades iniciales]
        ↓
[Venta: Pedido → Entrega → Factura]
        ↓
[Inventario se actualiza automáticamente]
```

La venta **descuenta automáticamente** las unidades del inventario al validar la entrega, mostrando así la integración entre módulos.

---

## Distribución sugerida de trabajo

| Integrante | Tarea sugerida |
|------------|---------------|
| — | Instalación de Odoo + configuración inicial |
| — | Crear catálogo de productos (categorías + 10 productos) |
| — | Ajuste de inventario (cantidades iniciales) |
| — | Demo de ventas (cliente + venta + validación) |
| — | Preparar presentación del roadmap |

> Asignen los nombres según disponibilidad de cada uno.

---

## Notas adicionales

- Usar la **misma base de datos** para que todo esté integrado.
- Tomar **capturas de pantalla** de cada paso para evidenciar el avance.
- El roadmap del Sprint 1 ya está documentado en el Word — solo llevarlo para mostrarlo.
- Si usan Odoo Online (prueba), asegúrense de exportar o guardar capturas antes de que venza el período de prueba.
