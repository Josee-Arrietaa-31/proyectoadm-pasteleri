# 🍞 Pan & Aroma - Guía de Instalación para Compañeros

## ⚙️ Requisitos Previos

1. **Docker Desktop** → https://www.docker.com/products/docker-desktop
2. **Git** → https://git-scm.com/downloads

**Una vez instalados, abre PowerShell o Terminal y sigue:**

---

## 🚀 3 Pasos Para Correr Odoo (5 minutos total)

### **Paso 1: Clonar Repositorio**

```powershell
git clone https://github.com/Josee-Arrietaa-31/proyectoadm-pasteleri.git
cd proyectoadm-pasteleri/odoo
```

### **Paso 2: Levantar Odoo**

```powershell
docker compose up -d
```

**Espera 20-30 segundos** a que se inicie.

### **Paso 3: Abrir Odoo**

Abre tu navegador en: **http://localhost:8069**

```
Email: andalfaro123@gmail.com
Contraseña: Gusano1199
```

**¡Listo! Ya está funcionando.** ✅

---

## ✅ Verifica que los Datos Estén Ahí

Una vez en Odoo, ve a:

1. **Inventario → Productos**
   - Deberías ver **30 productos**

2. **Ventas → Pedidos**
   - Deberías ver **1 orden** (S00001)

3. **Configuración → Compañías**
   - Deberías ver **Pan & Aroma**

Si ves todo esto, ¡**PERFECT**! 🎉

---

## 🛑 Para Detener Odoo

```powershell
cd proyectoadm-pasteleri/odoo
docker compose down
```

Los datos se guardan automáticamente en un volumen Docker.

---

## 🔄 Para Volver a Usar Después

```powershell
cd proyectoadm-pasteleri/odoo
docker compose up -d
```

Los datos estarán intactos.

---

## 📊 Datos Disponibles

- ✅ **30 productos** (pasteles, panes, repostería)
- ✅ **711 unidades** de stock
- ✅ **13 categorías** con 7 subcategorías de Pan
- ✅ **1 orden de venta** (S00001 - ₡11,300)
- ✅ **Pan & Aroma** empresa configurada

---

## ❌ Problemas Comunes

### "Docker daemon is not running"
→ Abre Docker Desktop

### "Port 8069 already in use"
→ Ejecuta: `docker compose down` y luego `docker compose up -d`

### "No veo los 30 productos"
→ Espera 30 segundos más. Si sigue sin aparecer, contacta al equipo.

---

## 🎓 Para la Presentación al Profesor

Mostrar en Odoo:
1. Inventario → Productos (30 items con descripción e imagen)
2. Inventario → Categorías (jerarquía con 7 subcategorías de Pan)
3. Ventas → Pedidos (orden S00001 confirmada)
4. Configuración → Compañías (Pan & Aroma con datos)

---

**¡Listo! Ya puedes demostrar el sistema.** 🎉
