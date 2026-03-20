import xmlrpc.client

url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

print("DIAGNÓSTICO COMPLETO DE LA BASE DE DATOS")
print("="*80)

# ── 1. VERIFICAR CONEXIÓN ────────────────────────────────────────────────────
print("\n1. VERIFICANDO CONEXIÓN A ODOO...")
try:
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    if uid:
        print(f"   ✅ Conexión exitosa. UID: {uid}")
    else:
        print("   ❌ Credenciales incorrectas")
        exit(1)
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    exit(1)

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

# ── 2. VERIFICAR ESTRUCTURA DE TABLAS ────────────────────────────────────────
print("\n2. VERIFICANDO ESTRUCTUTA DE DATOS...")

try:
    # Contar registros principales
    productos = call("product.template", "search_count", [[]])
    print(f"   ✅ Tabla producto.template: {productos} registros")
    
    categorias = call("product.category", "search_count", [[]])
    print(f"   ✅ Tabla product.category: {categorias} registros")
    
    ordenes = call("sale.order", "search_count", [[]])
    print(f"   ✅ Tabla sale.order: {ordenes} registros")
    
    clientes = call("res.partner", "search_count", [[["customer_rank", ">", 0]]])
    print(f"   ✅ Tabla res.partner (clientes): {clientes} registros")
    
    quants = call("stock.quant", "search_count", [[]])
    print(f"   ✅ Tabla stock.quant (inventario): {quants} registros")
    
except Exception as e:
    print(f"   ❌ Error al contar registros: {e}")
    exit(1)

# ── 3. VERIFICAR INTEGRIDAD DE DATOS ─────────────────────────────────────────
print("\n3. VERIFICANDO INTEGRIDAD DE DATOS...")

# Productos sin categoría
sin_categoria = call("product.template", "search", [[["categ_id", "=", False]]])
if sin_categoria:
    print(f"   ⚠️  {len(sin_categoria)} productos sin categoría")
else:
    print("   ✅ Todos los productos tienen categoría")

# Productos sin precio
sin_precio = call("product.template", "search", [[["list_price", "=", 0]]])
if sin_precio:
    print(f"   ⚠️  {len(sin_precio)} productos sin precio")
else:
    print("   ✅ Todos los productos tienen precio")

# Órdenes huérfanas (sin cliente)
ordenes_sin_cliente = call("sale.order", "search", [[["partner_id", "=", False]]])
if ordenes_sin_cliente:
    print(f"   ❌ {len(ordenes_sin_cliente)} órdenes sin cliente (PROBLEMA)")
else:
    print("   ✅ Todas las órdenes tienen cliente asignado")

# Órdenes sin líneas de producto
ordenes_vacias = call("sale.order", "search", [[["order_line", "=", []]]])
if ordenes_vacias:
    print(f"   ❌ {len(ordenes_vacias)} órdenes vacías (SIN PRODUCTOS)")
else:
    print("   ✅ Todas las órdenes tienen productos")

# ── 4. VERIFICAR RELACIONES ──────────────────────────────────────────────────
print("\n4. VERIFICANDO RELACIONES ENTRE TABLAS...")

try:
    # Verificar que cada producto tiene al menos una variante
    prods_sin_variante = call("product.template", "search", [[["product_variant_ids", "=", []]]])
    if prods_sin_variante:
        print(f"   ⚠️  {len(prods_sin_variante)} productos sin variantes")
    else:
        print("   ✅ Todos los productos tienen variantes")
    
    # Verificar categorías correctas
    cats_ok = call("product.category", "search_read", [], {"fields": ["id", "name", "parent_id"]})
    print(f"   ✅ {len(cats_ok)} categorías creadas correctamente")
    
except Exception as e:
    print(f"   ⚠️  Error verificando relaciones: {e}")

# ── 5. VERIFICAR STOCK ───────────────────────────────────────────────────────
print("\n5. VERIFICANDO INVENTARIO...")

try:
    stock_total = 0
    quants_data = call("stock.quant", "search_read", [], 
                       {"fields": ["product_id", "qty_available", "quantity"]})
    
    for quant in quants_data:
        stock_total += int(quant.get("qty_available", 0))
    
    print(f"   ✅ Stock total en sistema: {stock_total} unidades")
    
    if stock_total == 0:
        print("   ❌ PROBLEMA: No hay stock registrado")
    elif stock_total < 100:
        print("   ⚠️  Stock bajo (menos de 100 unidades)")
    else:
        print("   ✅ Stock adecuado")
        
except Exception as e:
    print(f"   ⚠️  Error verificando stock: {e}")

# ── 6. VERIFICAR EMPRESA ─────────────────────────────────────────────────────
print("\n6. VERIFICANDO INFORMACIÓN DE EMPRESA...")

try:
    empresa = call("res.company", "read", [call("res.company", "search", [[]])[0]], 
                   {"fields": ["name", "street", "city", "phone", "email"]})
    
    if empresa:
        emp = empresa[0]
        print(f"   ✅ Nombre: {emp.get('name', 'N/A')}")
        print(f"   ✅ Dirección: {emp.get('street', 'N/A')}, {emp.get('city', 'N/A')}")
        print(f"   ✅ Teléfono: {emp.get('phone', 'N/A')}")
        print(f"   ✅ Email: {emp.get('email', 'N/A')}")
    else:
        print("   ❌ No hay empresa configurada")
        
except Exception as e:
    print(f"   ❌ Error verificando empresa: {e}")

# ── 7. RESUMEN FINAL ─────────────────────────────────────────────────────────
print("\n" + "="*80)
print("RESUMEN DE DIAGNÓSTICO")
print("="*80)

print(f"\n📊 ESTADÍSTICAS:")
print(f"   • Productos: {productos}")
print(f"   • Categorías: {categorias}")
print(f"   • Órdenes de venta: {ordenes}")
print(f"   • Clientes: {clientes}")
print(f"   • Stock total: {stock_total} unidades")

print(f"\n✅ ESTADO: ", end="")
if (productos > 0 and categorias > 0 and stock_total > 0 and 
    not sin_categoria and not sin_precio and len(ordenes_sin_cliente) == 0):
    print("BASE DE DATOS OK ✓")
    print("\n   La base de datos está bien creada y tiene todos los datos.")
    print("   No se encontraron problemas críticos.")
else:
    print("REVISAR PROBLEMAS ⚠️")
    if sin_categoria or sin_precio:
        print("\n   ⚠️  Hay productos incompletos")
    if len(ordenes_sin_cliente) > 0:
        print(f"\n   ❌ Hay {len(ordenes_sin_cliente)} órdenes sin cliente")
    if stock_total == 0:
        print("\n   ❌ No hay stock registrado")

print("\n" + "="*80)
