# Instalación de Odoo Community — Windows
**Sistema Operativo:** Windows 10 / 11  
**Versión recomendada:** Odoo 17 Community (gratuita)  
**Fecha:** Marzo 2026

---

## Requisitos previos

- Computadora con Windows 10 u 11 (64 bits)
- Al menos **4 GB de RAM** libres
- Al menos **5 GB de espacio en disco**
- Conexión a internet para la descarga
- Navegador web (Chrome o Edge recomendado)

---

## Opción A — Instalador oficial de Windows (MÁS FÁCIL ✔)

### Paso 1 — Descargar Odoo

1. Ir a: **https://www.odoo.com/es/download**
2. En la sección "Community", seleccionar **Windows**.
3. Descargar el archivo `.exe` (aprox. 400–600 MB).

> El instalador de Windows incluye automáticamente:
> - Python
> - PostgreSQL (base de datos)
> - Odoo Server
> - Wkhtmltopdf (para reportes PDF)

---

### Paso 2 — Ejecutar el instalador

1. Hacer doble clic en el archivo `.exe` descargado.
2. Si Windows pide permiso de administrador → clic en **"Sí"**.
3. Seguir el asistente:

| Pantalla | Qué hacer |
|----------|-----------|
| Bienvenida | Clic en **Next** |
| Licencia | Aceptar → **Next** |
| Componentes | Dejar todo marcado → **Next** |
| Carpeta de instalación | Dejar la ruta por defecto → **Next** |
| Puerto | Dejar `8069` (por defecto) → **Next** |
| Contraseña del master | **IMPORTANTE:** Anotar la contraseña que asignen |
| Instalación | Esperar a que termine (puede tardar 5–10 min) |
| Finalizar | Clic en **Finish** |

---

### Paso 3 — Acceder a Odoo

1. Abrir el navegador web.
2. Escribir en la barra de direcciones:
   ```
   http://localhost:8069
   ```
3. Se abrirá la pantalla de creación de base de datos.

---

### Paso 4 — Crear la base de datos

Llenar el formulario con estos datos:

| Campo | Valor sugerido |
|-------|---------------|
| Master Password | (la que pusieron durante la instalación) |
| Database Name | `pasteleria_db` |
| Email | (su correo de administrador) |
| Password | (contraseña para ingresar a Odoo) |
| Language | **Spanish (ES)** |
| Country | **Costa Rica** |
| Demo data | **NO marcar** (queremos datos reales) |

4. Clic en **"Create database"**.
5. Esperar entre 1–3 minutos.
6. Odoo abrirá automáticamente el panel principal.

---

### Paso 5 — Instalar los módulos necesarios

Una vez dentro de Odoo:

1. Ir al menú principal (cuadrícula de apps arriba a la izquierda).
2. Buscar e instalar los siguientes módulos:

| Módulo | Para qué sirve |
|--------|---------------|
| **Inventario** (Inventory) | Gestión de productos y stock |
| **Ventas** (Sales) | Pedidos de venta y clientes |
| **Facturación** (Invoicing) | Facturas y pagos |

3. Para instalar: clic en el módulo → botón **"Instalar"** → esperar.

> ⚠️ Instalar de uno en uno para evitar errores.

---

### Paso 6 — Verificar que todo funciona

Después de instalar los módulos, confirmar que aparecen estos menús en la barra superior:
- ✅ Inventario
- ✅ Ventas
- ✅ Facturación

Si aparecen todos, la instalación fue exitosa.

---

## Opción B — Odoo Online (sin instalación, 15 días gratis)

Si no quieren instalar nada localmente:

1. Ir a: **https://www.odoo.com/es/trial**
2. Ingresar correo electrónico y nombre de la empresa (ej. "Pastelería Demo").
3. Seleccionar los módulos: **Inventario**, **Ventas**.
4. Odoo crea una instancia en la nube en minutos.
5. Acceden desde el navegador sin instalar nada.

> ⚠️ **Limitación:** Solo 15 días gratis. Si van a seguir usándolo en el proyecto, documenten todo con capturas.

---

## Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `http://localhost:8069` no carga | Verificar que el servicio "odoo-server-17" esté activo en los Servicios de Windows |
| Error al crear la base de datos | Intentar reiniciar el servicio de Odoo desde Servicios de Windows (Win + R → `services.msc`) |
| PostgreSQL no inicia | Ir a Servicios → buscar "postgresql" → clic derecho → Iniciar |
| Olvidaron la master password | Editar el archivo `C:\Program Files\Odoo 17.0\server\odoo.conf` y buscar `admin_passwd` |

---

## Iniciar/Detener Odoo manualmente (Windows)

Abrir PowerShell o CMD como administrador:

```powershell
# Iniciar Odoo
net start "odoo-server-17.0"

# Detener Odoo
net stop "odoo-server-17.0"

# Ver estado del servicio
Get-Service -Name "*odoo*"
```

---

## Próximos pasos después de instalar

1. ✅ Instalación completada
2. ⬜ Crear catálogo de productos (pasteles, pan, repostería)
3. ⬜ Registrar cantidades iniciales en Inventario
4. ⬜ Simular una venta de demo

---

## Datos de acceso para recordar

> Guardar estos datos en un lugar seguro

| Dato | Valor |
|------|-------|
| URL | http://localhost:8069 |
| Base de datos | pasteleria_db |
| Master Password | __________________ |
| Usuario admin | __________________ |
| Contraseña admin | __________________ |
