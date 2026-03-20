# 🎨 Instalación del Tema Pan & Aroma - CSS Personalizado

## ✅ Módulo Creado
La carpeta personalizada **`custom_theme`** ya está lista en:
```
odoo/custom_theme/
├── __manifest__.py        (Definición del módulo)
├── __init__.py
└── static/
    ├── description/
    │   └── index.html
    └── src/
        └── css/
            ├── theme.css           (Estilos backend - 5.5KB)
            └── website_theme.css   (Estilos frontend - 2.2KB)
```

## 🎨 Colores Aplicados (Pan & Aroma)

| Elemento | Color | Hex |
|----------|-------|-----|
| Principal | Marrón Pastel | #D4956E |
| Secundario | Beige Claro | #E8D4C4 |
| Acento | Marrón Oscuro | #C67C4E |
| Fondo Claro | Crema | #F5F0EB |
| Texto Oscuro | Marrón Oscuro | #6B4423 |

## 📦 Instalación Manual en Odoo

### **Opción 1: Instalación Automática (Recomendada)**

1. **Abre Odoo** en tu navegador: http://localhost:8069
2. **Inicia sesión** con:
   - Email: `andalfaro123@gmail.com`
   - Contraseña: `Gusano1199`

3. **Ve a Aplicaciones → Apps**

4. **En la esquina superior derecha, busca el icono de actualización ⟳**
   - Click en: **Actualizar lista**
   - Espera a que termine (puede tomar 30 segundos)

5. **Busca en la barra de búsqueda:**
   - Escribe: `Pan & Aroma`

6. **Haz click en "Pan & Aroma - Tema Personalizado"**
   - Luego en el botón verde **"Instalar"**

7. **Espera a que se instale**

8. **¡Listo!** Actualiza la página (F5 o Ctrl+R) y verás los nuevos colores

### **Opción 2: Instalación Manual (Si la automática no funciona)**

1. Abre una terminal PowerShell en la carpeta del proyecto

2. Ejecuta estos comandos:
```powershell
# Entrar a la carpeta de trabajo
cd "c:\Users\josea\OneDrive - Estudiantes ITCR\semestre#5-2026\Admin.Proyectos\proyectoadm"

# Verificar que Odoo está corriendo
docker ps

# Detener Odoo
docker compose down

# Copiar el módulo a la ubicación correcta en Docker
docker cp "odoo/custom_theme" odoo-web-1:/mnt/extra-addons/

# Reiniciar Odoo
docker compose up -d

# Esperar 20 segundos
Start-Sleep -Seconds 20

# Luego ir a Odoo y instalar manualmente (pasos 1-8 arriba)
```

## 🎯 Cambios que Verás

El sistema cambiará de interfaz con:

### **Backend (Panel de Control)**
- ✅ Botones principales en marrón pastel
- ✅ Menú lateral con colores Pan & Aroma
- ✅ Tablas con encabezados en beige
- ✅ Campos enfocados con bordes en marrón
- ✅ Modales con headers personalizados
- ✅ Alertas y notificaciones con tema

### **Frontend (Tienda Online)**
- ✅ Navegación en marrón principal
- ✅ Botones de compra personalizados
- ✅ Cards de productos con hover effects
- ✅ Footer con colores coordenados

## 🔧 Personalización Adicional

Si quieres cambiar los colores, edita los archivos:

```bash
# Para Backend:
odoo/custom_theme/static/src/css/theme.css

# Para Website:
odoo/custom_theme/static/src/css/website_theme.css
```

Busca las líneas con `:root` y modifica los valores hexadecimales.

## ✅ Verificación

Después de instalar, verifica que:
- [ ] Los botones son marrón pastel (#D4956E)
- [ ] El menú lateral tiene colores Pan & Aroma
- [ ] Las tablas tienen encabezados en beige
- [ ] Los inputs enfocados tienen borde marrón
- [ ] Acordeón/Tabs usan los colores personalizados

## 📞 Soporte

Si algo no funciona:
1. Limpia el caché del navegador (Ctrl+Shift+Del)
2. Cierra y abre de nuevo Odoo
3. Recarga la página Odoo (Ctrl+F5)
4. Reinicia el contenedor: `docker restart odoo-web-1`

¡Listo! 🎉
