import xmlrpc.client

url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

print("VERIFICACIÓN DE STOCK EN DETALLE")
print("="*80)

# Obtener todos los productos
productos = call("product.product", "search_read", [], {
    "fields": ["id", "name", "qty_available", "virtual_available"]
})

print(f"Total de productos (variantes): {len(productos)}\n")

stock_total = 0
productos_con_stock = 0
productos_sin_stock = 0

print("Lista de productos y su stock:")
print("-" * 80)
for prod in productos:
    qty = int(prod.get("qty_available", 0))
    stock_total += qty
    if qty > 0:
        productos_con_stock += 1
        print(f"  ✅ {prod['name']}: {qty} unidades")
    else:
        productos_sin_stock += 1

print("-" * 80)
print(f"\n📊 RESUMEN:")
print(f"   • Productos con stock: {productos_con_stock}")
print(f"   • Productos sin stock: {productos_sin_stock}")
print(f"   • Stock total: {stock_total} unidades")

if stock_total == 0:
    print("\n⚠️  PROBLEMA DETECTADO:")
    print("   Los productos existen pero NO tienen stock registrado.")
    print("   Los scripts de stock no se guardaron correctamente.")
    print("\n💡 SOLUCIÓN:")
    print("   Voy a regenerar el stock de todos los productos.")
else:
    print(f"\n✅ Stock OK: {stock_total} unidades registradas")
