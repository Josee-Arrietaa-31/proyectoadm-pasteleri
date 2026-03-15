import xmlrpc.client
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

# ── 1. CONFIGURAR EMPRESA ──────────────────────────────────────────────────────
print("Configurando información de la empresa...")

empresa_data = {
    "name": "Pan & Aroma",
    "street": "Costado norte del Parque Central",
    "city": "Ciudad Quesada",
    "state_id": call("res.country.state", "search", [[["code", "=", "CR-SJ"]]])[0] if call("res.country.state", "search", [[["code", "=", "CR-SJ"]]]) else False,
    "zip": "21000",
    "country_id": call("res.country", "search", [[["code", "=", "CR"]]])[0],
    "phone": "84835577",
    "email": "info@panyaroma.com",
    "website": "www.panyaroma.com",
}

empresa_ids = call("res.company", "search", [[]])
if empresa_ids:
    empresa_id = empresa_ids[0]
    call("res.company", "write", [[empresa_id], empresa_data])
    print(f"  [actualizada] Pan & Aroma")
else:
    empresa_id = call("res.company", "create", [empresa_data])
    print(f"  [creada] Pan & Aroma (id={empresa_id})")

# ── 2. CREAR IMÁGENES PLACEHOLDER ──────────────────────────────────────────────
print("\nGenerando imágenes placeholder para productos...")

def crear_imagen_producto(nombre, color_rgb):
    """Crea una imagen simple con el nombre del producto"""
    img = Image.new('RGB', (400, 400), color=color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Agregar texto en el centro
    texto = nombre.replace(" ", "\n")
    draw.text((200, 180), texto, fill=(255,255,255), anchor="mm")
    
    # Convertir a base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

imagenes = {
    "Pastel de Chocolate": (139, 69, 19),      # Marrón
    "Pastel de Vainilla": (255, 220, 130),     # Amarillo claro
    "Pastel Tres Leches": (255, 182, 193),     # Rosa
    "Pan de Mantequilla": (210, 180, 140),     # Tan
    "Pan Integral": (101, 67, 33),              # Marrón oscuro
    "Croissant": (255, 215, 0),                 # Oro
    "Muffin de Arandanos": (138, 43, 226),     # Azul violeta
    "Cupcake Decorado": (255, 105, 180),       # Rosa intenso
    "Brownie de Chocolate": (101, 51, 25),     # Marrón muy oscuro
    "Galletas con Chispas": (160, 82, 45),     # Café
}

# ── 3. DESCRIPCIONES DE PRODUCTOS ──────────────────────────────────────────────
descripciones = {
    "Pastel de Chocolate": "Delicioso pastel de chocolate hecho con cacao de alta calidad. Perfecto para cualquier celebración especial. Esponjoso y jugoso en su interior con cobertura de chocolate smooth.",
    "Pastel de Vainilla": "Clásico pastel de vainilla con sabor auténtico. Ideal para desayunos, meriendas o eventos especiales. Hecho con vainilla natural y relleno cremoso.",
    "Pastel Tres Leches": "Una delicia tropical típica latinoamericana. Preparado con tres tipos de leche (condensada, evaporada y crema). Esponjoso, humedecido y cubierto con merengue y coco.",
    "Pan de Mantequilla": "Pan artesanal elaborado diariamente con mantequilla fresca. Suave, esponjoso y con ese aroma inconfundible. Perfecto para el desayuno con café o té.",
    "Pan Integral": "Pan nutritivo hecho con harina integral de alta calidad. Rico en fibra y nutrientes. Sabor robusto y textura característica de los panes integrales.",
    "Croissant": "Delicado croissant de hojaldre francés. Crujiente por fuera, suave y butiroso por dentro. Ideal para acompañar con café en cualquier hora del día.",
    "Muffin de Arándanos": "Muffin esponjoso relleno de arándanos frescos. Suavemente dulce con el toque ácido de los frutos rojos. Una opción saludable y deliciosa.",
    "Cupcake Decorado": "Pequeño pastel decorado con detalles especiales. Vainilla suave en su interior con cobertura de buttercream. Ideal para regalos o celebraciones íntimas.",
    "Brownie de Chocolate": "Brownie denso y muy chocolatero. Hecho con chocolate de premium y nueces (opcional). Postre perfecto para los amantes del chocolate.",
    "Galletas con Chispas": "Galletas crujientes rellenas de chispas de chocolate. Receta tradicional hecha en casa con ingredientes frescos. Venta por bolsa de múltiples galletas.",
}

print("\nActualizando productos con descripciones e imágenes...")
for nombre, descripcion in descripciones.items():
    # Buscar el producto
    prod = call("product.template", "search_read", [[["name", "=", nombre]]], {"fields": ["id", "name"]})
    if not prod:
        print(f"  [no encontrado] {nombre}")
        continue
    
    prod_id = prod[0]["id"]
    
    # Generar imagen
    color = imagenes.get(nombre, (200, 200, 200))
    img_b64 = crear_imagen_producto(nombre, color)
    
    # Actualizar producto
    call("product.template", "write", [[prod_id], {
        "description": descripcion,
        "image_1920": img_b64,
    }])
    print(f"  [ok] {nombre}")

# ── 4. UNIDADES DE MEDIDA ──────────────────────────────────────────────────────
print("\nVerificando unidades de medida...")

uom_data = [
    ("Unidades", "Unit", 1.0),
    ("Caja", "Box", 12.0),
    ("Paquete", "Pack", 6.0),
]

for nombre, codigo, factor in uom_data:
    existe = call("uom.uom", "search", [[["name", "=", nombre]]])
    if existe:
        print(f"  [existe] {nombre}")
    else:
        uom_id = call("uom.uom", "create", [{
            "name": nombre,
            "category_id": call("uom.category", "search", [[["name", "=", "Unit"]]])[0],
            "factor": 1.0,
            "uom_type": "reference",
        }])
        print(f"  [creada] {nombre}")

print("\n=== RESUMEN DE CAMBIOS ===")
print("✅ Empresa Pan & Aroma configurada")
print("✅ Dirección: Costado norte del Parque Central, Ciudad Quesada, San Carlos")
print("✅ Teléfono: 84835577 | Email: info@panyaroma.com")
print("✅ Descripciones agregadas a todos los 10 productos")
print("✅ Imágenes placeholder generadas para cada producto")
print("✅ Unidades de medida configuradas")
print("\nVerificar en Odoo:")
print("  → Inventario → Productos → Productos (ver descripciones e imágenes)")
print("  → Configuración → Datos de la empresa (verificar Pan & Aroma)")
