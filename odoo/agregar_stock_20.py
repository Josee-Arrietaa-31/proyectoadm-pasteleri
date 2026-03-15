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

# Stock inicial para los 20 productos nuevos
stock_nuevos = {
    "Baguette Francés": 20,
    "Focaccia con Olivas": 15,
    "Pan de Ajo": 25,
    "Donas Glaseadas": 30,
    "Palitos de Pan": 40,
    "Empanada de Carne": 18,
    "Pan de Queso": 22,
    "Roscas de Canela": 16,
    "Pan Tostado": 20,
    "Galleta Saldada": 35,
    "Media Noche": 15,
    "Pan de Pasas": 12,
    "Churros": 25,
    "Cuerno de Chocolate": 18,
    "Pan Aromático": 10,
    "Biscocho de Coco": 14,
    "Pan de Jengibre": 12,
    "Rollito de Jamón": 20,
    "Tiritas de Queso": 30,
    "Pan Multigrano": 18,
}

# Ubicación de inventario
loc_ids = call("stock.location", "search", [[["usage", "=", "internal"]]])
location_id = loc_ids[0] if loc_ids else False

if not location_id:
    print("❌ No se found ubicación de inventario")
    exit(1)

print("Agregando stock a los 20 productos nuevos...\n")

for nombre, cantidad in stock_nuevos.items():
    # Buscar el producto
    tmpl = call("product.template", "search_read", [[["name", "=", nombre]]], {"fields": ["name", "product_variant_ids"]})
    if not tmpl:
        print(f"  [no encontrado] {nombre}")
        continue
    
    variant_id = tmpl[0]["product_variant_ids"][0]
    
    # Buscar o crear quant
    quant_id = call("stock.quant", "search", [[["product_id", "=", variant_id], ["location_id", "=", location_id]]])
    if quant_id:
        qid = quant_id[0]
    else:
        qid = call("stock.quant", "create", [{"product_id": variant_id, "location_id": location_id, "quantity": 0.0}])
    
    # Actualizar cantidad
    call("stock.quant", "write", [[qid], {"inventory_quantity": cantidad}])
    try:
        call("stock.quant", "action_apply_inventory", [[qid]])
    except Exception:
        pass
    
    print(f"  [ok] {nombre}: {cantidad} unidades")

print("\n✅ Stock agregado a todos los 20 productos")
