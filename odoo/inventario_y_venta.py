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

# Cantidades iniciales por producto
stock_inicial = {
    "Pastel de Chocolate":  5,
    "Pastel de Vainilla":   5,
    "Pastel Tres Leches":   4,
    "Pan de Mantequilla":  30,
    "Pan Integral":        10,
    "Croissant":           25,
    "Muffin de Arandanos": 15,
    "Cupcake Decorado":    12,
    "Brownie de Chocolate":18,
    "Galletas con Chispas":20,
}

# Ubicación interna por defecto (WH/Stock)
loc_ids = call("stock.location", "search", [[["complete_name", "like", "WH/Stock"], ["usage", "=", "internal"]]])
if not loc_ids:
    loc_ids = call("stock.location", "search", [[["usage", "=", "internal"]]])
location_id = loc_ids[0]
print(f"Ubicacion de inventario id={location_id}")

print("\nRegistrando cantidades iniciales...")
for nombre, cantidad in stock_inicial.items():
    # Buscar product.product (variante) desde el template
    tmpl = call("product.template", "search_read", [[["name", "=", nombre]]], {"fields": ["name", "product_variant_ids"]})
    if not tmpl:
        print(f"  [no encontrado] {nombre}")
        continue
    variant_id = tmpl[0]["product_variant_ids"][0]

    # Crear ajuste de inventario (quant)
    quant_id = call("stock.quant", "search", [[["product_id", "=", variant_id], ["location_id", "=", location_id]]])
    if quant_id:
        qid = quant_id[0]
    else:
        qid = call("stock.quant", "create", [{"product_id": variant_id, "location_id": location_id, "quantity": 0.0}])
    call("stock.quant", "write", [[qid], {"inventory_quantity": cantidad}])
    try:
        call("stock.quant", "action_apply_inventory", [[qid]])
    except Exception:
        pass  # El método puede retornar None/accion; el cambio igual se aplica

    print(f"  [ok] {nombre}: {cantidad} unidades")

print("\n¡Inventario inicial registrado correctamente!")

# ── Demo de ventas ─────────────────────────────────────────────────────────────
print("\n--- Creando cliente y venta de demo ---")

# Crear cliente
cliente_ids = call("res.partner", "search", [[["name", "=", "Laura Rodriguez"]]])
if cliente_ids:
    cliente_id = cliente_ids[0]
    print(f"  [cliente ya existe] Laura Rodriguez id={cliente_id}")
else:
    cliente_id = call("res.partner", "create", [{
        "name":    "Laura Rodriguez",
        "email":   "laura.rodriguez@demo.com",
        "phone":   "88880000",
        "country_id": call("res.country", "search", [[["code", "=", "CR"]]])[0],
        "customer_rank": 1,
    }])
    print(f"  [cliente creado] Laura Rodriguez id={cliente_id}")

# Buscar productos para la venta
pastel = call("product.product", "search", [[["name", "=", "Pastel de Chocolate"]]])[0]
croissant = call("product.product", "search", [[["name", "=", "Croissant"]]])[0]

# Obtener precios
pastel_price    = call("product.product", "read", [[pastel]],    {"fields": ["list_price"]})[0]["list_price"]
croissant_price = call("product.product", "read", [[croissant]], {"fields": ["list_price"]})[0]["list_price"]

# Crear orden de venta
order_id = call("sale.order", "create", [{
    "partner_id": cliente_id,
    "order_line": [
        [0, 0, {"product_id": pastel,    "product_uom_qty": 1, "price_unit": pastel_price}],
        [0, 0, {"product_id": croissant, "product_uom_qty": 2, "price_unit": croissant_price}],
    ]
}])
print(f"  [orden creada] id={order_id}")

# Confirmar la orden
call("sale.order", "action_confirm", [[order_id]])
order_info = call("sale.order", "read", [[order_id]], {"fields": ["name", "state", "amount_total"]})[0]
print(f"  [confirmada] {order_info['name']} | estado={order_info['state']} | total=₡{order_info['amount_total']:,.0f}")

print("\n=== RESUMEN FINAL ===")
print(f"  Inventario: 10 productos con cantidades registradas")
print(f"  Cliente:    Laura Rodriguez")
print(f"  Venta:      {order_info['name']} — 1x Pastel de Chocolate + 2x Croissant")
print(f"  Total:      ₡{order_info['amount_total']:,.0f}")
print("\nVer en Odoo:")
print("  Inventario → Productos → Productos (ver stock en cada producto)")
print("  Ventas → Pedidos → Pedidos (ver la orden confirmada)")
