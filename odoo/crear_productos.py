import xmlrpc.client

# Configuración de conexión
url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

print("Conectando a Odoo...")
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})

if not uid:
    print("ERROR: Credenciales incorrectas o base de datos no encontrada.")
    exit(1)

print(f"Conexion exitosa. UID: {uid}")
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

# ── 1. Categorías ──────────────────────────────────────────────────────────────
print("\nCreando categorias de producto...")

# Buscar categoría raíz "All"
all_cat = call("product.category", "search", [[["name", "=", "All"]]])
parent_id = all_cat[0] if all_cat else False

categorias = ["Pasteles", "Pan", "Repostería"]
cat_ids = {}

for nombre in categorias:
    existe = call("product.category", "search", [[["name", "=", nombre]]])
    if existe:
        cat_ids[nombre] = existe[0]
        print(f"  [ya existe] {nombre}")
    else:
        cid = call("product.category", "create", [{"name": nombre, "parent_id": parent_id}])
        cat_ids[nombre] = cid
        print(f"  [creada] {nombre} (id={cid})")

# ── 2. Productos ───────────────────────────────────────────────────────────────
print("\nCreando productos...")

productos = [
    {"name": "Pastel de Chocolate",  "categ": "Pasteles",   "price": 8500},
    {"name": "Pastel de Vainilla",   "categ": "Pasteles",   "price": 7500},
    {"name": "Pastel Tres Leches",   "categ": "Pasteles",   "price": 9000},
    {"name": "Pan de Mantequilla",   "categ": "Pan",        "price": 350},
    {"name": "Pan Integral",         "categ": "Pan",        "price": 1200},
    {"name": "Croissant",            "categ": "Pan",        "price": 750},
    {"name": "Muffin de Arandanos",  "categ": "Repostería", "price": 900},
    {"name": "Cupcake Decorado",     "categ": "Repostería", "price": 1200},
    {"name": "Brownie de Chocolate", "categ": "Repostería", "price": 850},
    {"name": "Galletas con Chispas", "categ": "Repostería", "price": 1800},
]

for p in productos:
    existe = call("product.template", "search", [[["name", "=", p["name"]]]])
    if existe:
        print(f"  [ya existe] {p['name']}")
        continue

    pid = call("product.template", "create", [{
        "name":        p["name"],
        "categ_id":    cat_ids[p["categ"]],
        "list_price":  p["price"],
        "type":        "product",      # Almacenable
        "sale_ok":     True,
        "purchase_ok": True,
    }])
    print(f"  [creado] {p['name']} - ₡{p['price']:,} (id={pid})")

print("\n¡Listo! Todos los productos fueron creados.")
print("Verificar en Odoo: Inventario → Productos → Productos")
