#!/usr/bin/env python3
"""
Script para instalar y activar el módulo custom_theme en Odoo
Pan & Aroma - Tema Personalizado
"""

import xmlrpc.client
import sys

# Configuración
url = "http://localhost:8069"
db = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

try:
    # Conectar a Odoo
    print("🔗 Conectando a Odoo...")
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("❌ Error: No se pudo autenticar")
        sys.exit(1)
    
    print(f"✅ Autenticación exitosa (UID: {uid})")
    
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    
    # Buscar el módulo custom_theme
    print("\n🔍 Buscando módulo 'custom_theme'...")
    modules = models.execute_kw(
        db, uid, password, 'ir.module.module', 'search',
        [[['name', '=', 'custom_theme']]]
    )
    
    if not modules:
        print("⚠️  Módulo 'custom_theme' no encontrado en Odoo")
        print("   Asegúrate de que la carpeta 'custom_theme' esté en:")
        print("   /odoo/addons/custom_theme/")
        print("\n   Pasos:")
        print("   1. Copia la carpeta 'custom_theme' a: /odoo/addons/")
        print("   2. Reinicia Odoo: docker restart odoo-web-1")
        print("   3. Ve a Aplicaciones → Actualizar lista")
        print("   4. Busca 'Pan & Aroma' e instala 'Pan & Aroma - Tema Personalizado'")
        sys.exit(1)
    
    module_id = modules[0]
    print(f"✅ Módulo encontrado (ID: {module_id})")
    
    # Obtener estado del módulo
    module_data = models.execute_kw(
        db, uid, password, 'ir.module.module', 'read',
        [module_id], ['name', 'state']
    )
    
    current_state = module_data[0]['state']
    print(f"   Estado actual: {current_state}")
    
    # Si no está instalado, instalarlo
    if current_state != 'installed':
        print("\n📦 Instalando módulo...")
        models.execute_kw(
            db, uid, password, 'ir.module.module', 'button_install',
            [module_id]
        )
        print("✅ Módulo instalado exitosamente")
    else:
        print("ℹ️  El módulo ya está instalado")
    
    # Upgrade (actualizar cambios si es necesario)
    print("\n🔄 Aplicando cambios...")
    models.execute_kw(
        db, uid, password, 'ir.module.module', 'button_upgrade',
        [module_id]
    )
    print("✅ Cambios aplicados")
    
    print("\n" + "="*50)
    print("✅ ¡ÉXITO! Tema Pan & Aroma instalado")
    print("="*50)
    print("\n📝 Próximos pasos:")
    print("1. Actualiza la página de Odoo (F5 o Ctrl+R)")
    print("2. Verifica que los colores hayan cambiado")
    print("3. Si no ves cambios, limpia el caché del navegador")
    print("\n🎨 Colores aplicados:")
    print("   - Primario: #D4956E (Marrón pastel)")
    print("   - Secundario: #E8D4C4 (Beige claro)")
    print("   - Acento: #C67C4E (Marrón oscuro)")
    print("\n")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    sys.exit(1)
