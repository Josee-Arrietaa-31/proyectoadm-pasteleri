# 🍞 Pan & Aroma - Guía de Instalación para Compañeros

## ⚙️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **Docker Desktop** (incluye Docker y Docker Compose)
  - Windows: https://www.docker.com/products/docker-desktop
  - Mac/Linux: https://www.docker.com/products/docker-desktop
- **Git** (para clonar el repositorio)
  - https://git-scm.com/downloads
- **PowerShell** (en Windows) o **Terminal** (Mac/Linux)

## 📥 Paso 1: Clonar el Repositorio

Abre una terminal/PowerShell y ejecuta:

```powershell
git clone https://github.com/Josee-Arrietaa-31/proyectoadm-pasteleri.git
cd proyectoadm-pasteleri
```

## 🚀 Paso 2: Levantar Odoo con Docker

### En Windows (PowerShell):

```powershell
cd odoo
docker compose up -d
```

### En Mac/Linux (Terminal):

```bash
cd odoo
docker compose up -d
```

**Espera 20-30 segundos** a que Docker inicie los contenedores.

## ✅ Verificar que Está Funcionando

```powershell
docker ps
```

Deberías ver 2 contenedores corriendo:
- `odoo-web-1` (puerto 8069)
- `odoo-db-1` (PostgreSQL)

## 🌐 Acceder a Odoo

Abre tu navegador en:

```
http://localhost:8069
```

### Credenciales por Defecto:

| Campo | Valor |
|-------|-------|
| Email | `andalfaro123@gmail.com` |
| Contraseña | `Gusano1199` |

## 📊 Verifica que los Datos Estén Cargados

Una vez dentro de Odoo:

1. **Ve a Inventario → Productos**
   - Deberías ver **30 productos** (pasteles, panes, repostería)

2. **Ve a Ventas → Pedidos**
   - Deberías ver **1 pedido** (S00001 de Laura Rodríguez por ₡11,300)

3. **Ve a Configuración → Compañías**
   - Deberías ver **Pan & Aroma** con dirección y contacto

Si ves todo esto, ¡**ÉXITO**! La BD está lista.

---

## 🛑 Detener Odoo

Cuando termines, ejecuta:

```powershell
cd odoo
docker compose down
```

Esto detiene los contenedores pero **mantiene los datos locales** en el volumen Docker.

---

## 🔄 Levantar de Nuevo

Para volver a usar Odoo después:

```powershell
cd proyectoadm-pasteleri/odoo
docker compose up -d
```

Los datos estarán intactos porque están en un volumen persistente.

---

## ⚠️ Problemas Comunes

### Error: "Docker daemon is not running"
**Solución:** Abre Docker Desktop (debe estar ejecutándose antes de usar Docker)

### Error: "Port 8069 already in use"
**Solución:** Otro servicio está usando ese puerto. Ejecuta:
```powershell
docker compose down
docker compose up -d
```

### Odoo no abre (errores de conexión)
**Solución:** Espera más tiempo. A veces tarda 30-40 segundos en estar listo.

### No veo los 30 productos
**Solución:** La BD podría no estar restaurada correctamente. Contacta al equipo de desarrollo.

---

## 📁 Estructura del Proyecto

```
proyectoadm-pasteleri/
├── odoo/                          ← AQUÍ está todo
│   ├── docker-compose.yml         ← Configuración Docker
│   ├── config/
│   │   └── odoo.conf              ← Credenciales Odoo
│   ├── custom_theme/              ← Tema personalizado (opcional)
│   ├── crear_productos.py         ← Scripts de datos
│   ├── diagnostico_bd.py          ← Verificación BD
│   └── ...otros scripts...
├── .git/                          ← Control de versiones
├── README.md                       ← Este archivo
└── ...
```

---

## 🎓 Para la Presentación al Profesor

**Lo que mostrar en Odoo:**

1. **Inventario → Productos** - 30 productos con descripciones
2. **Inventario → Categorías** - 7 subcategorías de Pan
3. **Ventas → Pedidos** - Orden S00001 confirmada
4. **Dashboard** - Widgets con información de empresa
5. **Configuración → Compañías** - Pan & Aroma con datos completos

---

## 📞 Contacto

Si hay problemas:
- Revisa el archivo `INSTRUCTIVO_COMPANEROS_ODOO.md`
- Contacta al equipo de desarrollo del proyecto

---

**¡Listo! Ahora puedes demostrar el sistema Odoo funcional.** 🎉
