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

# Buscar la categoría "Pan" como padre
cat_pan = call("product.category", "search", [[["name", "=", "Pan"]]])
if not cat_pan:
    print("❌ Categoría 'Pan' no encontrada")
    exit(1)

cat_pan_id = cat_pan[0]

print("Creando subcategorías de Pan...\n")

# Nuevas subcategorías
subcategorias = [
    "Panes Integrales",
    "Panes Dulces",
    "Panes Gourmet",
    "Panes Salados",
    "Panes de Relleno",
    "Acompañamientos",
    "Horneados Artesanales",
]

cat_ids = {}

for nombre in subcategorias:
    # Verificar si ya existe
    existe = call("product.category", "search", [[["name", "=", nombre], ["parent_id", "=", cat_pan_id]]])
    if existe:
        cat_ids[nombre] = existe[0]
        print(f"  [existe] {nombre}")
    else:
        cat_id = call("product.category", "create", [{
            "name": nombre,
            "parent_id": cat_pan_id,
        }])
        cat_ids[nombre] = cat_id
        print(f"  [creada] {nombre}")

# ── Reasignar productos a categorías ───────────────────────────────────────────
print("\nReasignando productos a categorías...\n")

asignaciones = {
    "Panes Integrales": [
        "Pan Integral",
        "Pan Multigrano",
        "Pan Aromático",
    ],
    "Panes Dulces": [
        "Media Noche",
        "Pan de Pasas",
        "Roscas de Canela",
        "Pan de Jengibre",
        "Biscocho de Coco",
    ],
    "Panes Gourmet": [
        "Baguette Francés",
        "Focaccia con Olivas",
        "Pan Aromático",
    ],
    "Panes Salados": [
        "Pan de Ajo",
        "Pan de Queso",
        "Galleta Saldada",
        "Tiritas de Queso",
    ],
    "Panes de Relleno": [
        "Empanada de Carne",
        "Cuerno de Chocolate",
        "Rollito de Jamón",
    ],
    "Acompañamientos": [
        "Palitos de Pan",
        "Pan Tostado",
    ],
    "Horneados Artesanales": [
        "Donas Glaseadas",
        "Churros",
        "Croissant",
    ],
}

for categoria, productos in asignaciones.items():
    cat_id = cat_ids[categoria]
    for nombre_prod in productos:
        # Buscar producto
        prod = call("product.template", "search", [[["name", "=", nombre_prod]]])
        if prod:
            prod_id = prod[0]
            call("product.template", "write", [[prod_id], {"categ_id": cat_id}])
            print(f"  ✓ {nombre_prod} → {categoria}")
        else:
            print(f"  ✗ {nombre_prod} (no encontrado)")

print("\n" + "="*70)
print("✅ CATEGORÍAS CREADAS Y PRODUCTOS ORGANIZADOS")
print("="*70)
print("\nEstructura de Categorías:")
print("\n📁 Pan/")
for cat in subcategorias:
    productos_asignados = asignaciones.get(cat, [])
    print(f"  ├─ {cat}")
    for prod in productos_asignados:
        print(f"  │  └─ {prod}")

print("\n\nVer en Odoo:")
print("  Inventario → Productos → Categorías (ver jerarquía)")
print("  Inventario → Productos → Productos (filtrar por categoría)")
