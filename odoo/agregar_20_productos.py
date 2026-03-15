import xmlrpc.client
import base64
from io import BytesIO
from PIL import Image, ImageDraw

url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

def crear_imagen_producto(nombre, color_rgb):
    img = Image.new('RGB', (400, 400), color=color_rgb)
    draw = ImageDraw.Draw(img)
    texto = nombre.replace(" ", "\n")
    draw.text((200, 180), texto, fill=(255,255,255), anchor="mm")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

# Buscar categoría "Pan"
cat_pan = call("product.category", "search", [[["name", "=", "Pan"]]])
cat_pan_id = cat_pan[0] if cat_pan else False

if not cat_pan_id:
    print("❌ Categoría 'Pan' no encontrada")
    exit(1)

print("Agregando 20 productos de panadería...\n")

productos_nuevos = [
    {"name": "Baguette Francés", "price": 2500, "color": (210, 180, 140), "desc": "Auténtica baguette francesa crujiente por fuera, suave por dentro. Ideal para sándwiches o acompañamiento."},
    {"name": "Focaccia con Olivas", "price": 2200, "color": (184, 134, 11), "desc": "Pan plano italiano con olivas y orégano. Perfecta para abrir y rellenar o comer sola."},
    {"name": "Pan de Ajo", "price": 1800, "color": (160, 82, 45), "desc": "Pan crujiente con mantequilla y ajo casero. Excelente complemento para comidas."},
    {"name": "Donas Glaseadas", "price": 1200, "color": (255, 165, 0), "desc": "Donas esponjosas cubiertas con glaseado azucarado. Perfectas para desayuno o merienda."},
    {"name": "Palitos de Pan", "price": 800, "color": (205, 133, 63), "desc": "Delgados y crujientes. Ideales para acompañar sopa o como snack."},
    {"name": "Empanada de Carne", "price": 2000, "color": (139, 69, 19), "desc": "Rellena de carne molida con especias. Lista para comer o calentar."},
    {"name": "Pan de Queso", "price": 1500, "color": (255, 218, 185), "desc": "Pan suave con queso fundido en su interior. Delicioso y sabroso."},
    {"name": "Roscas de Canela", "price": 1600, "color": (210, 105, 30), "desc": "Enrolladas con canela y azúcar. Aromáticas y deliciosas."},
    {"name": "Pan Tostado", "price": 1100, "color": (184, 134, 11), "desc": "Pan integral tostado y cortado. Perfecto para dips o untables."},
    {"name": "Galleta Saldada", "price": 900, "color": (195, 176, 145), "desc": "Galleta crujiente con sal marina. Acompañante perfecto para queso."},
    {"name": "Media Noche", "price": 1900, "color": (218, 165, 32), "desc": "Pan marrón dulce y suave. Ideal para desayuno o merienda con mermelada."},
    {"name": "Pan de Pasas", "price": 2100, "color": (188, 143, 143), "desc": "Pan de trigo relleno de pasas de uva. Nutritivo y sabroso."},
    {"name": "Churros", "price": 1300, "color": (255, 215, 0), "desc": "Churros recién hechos. Ideales para acompañar chocolate caliente."},
    {"name": "Cuerno de Chocolate", "price": 2000, "color": (139, 69, 19), "desc": "Croissant con chocolate derretido en su interior. Exquisito y sabroso."},
    {"name": "Pan Aromático", "price": 2300, "color": (160, 82, 45), "desc": "Pan con semillas, nueces y especies. Completo y aromático."},
    {"name": "Biscocho de Coco", "price": 1700, "color": (240, 230, 200), "desc": "Bizcocho con coco rallado. Tropical y delicioso."},
    {"name": "Pan de Jengibre", "price": 1900, "color": (184, 134, 11), "desc": "Pan especiado con jengibre fresco. Perfecto para las tardes frías."},
    {"name": "Rollito de Jamón", "price": 2200, "color": (210, 180, 140), "desc": "Rollito de hojaldre relleno de jamón y queso. Práctico y sabroso."},
    {"name": "Tiritas de Queso", "price": 1100, "color": (255, 218, 185), "desc": "Tiras crujientes de queso gratinado. Snack irresistible."},
    {"name": "Pan Multigrano", "price": 1400, "color": (139, 90, 43), "desc": "Pan con múltiples granos y semillas. Nutritivo y saludable."},
]

conteo = 0
for prod in productos_nuevos:
    # Verificar si ya existe
    existe = call("product.template", "search", [[["name", "=", prod["name"]]]])
    if existe:
        print(f"  [ya existe] {prod['name']}")
        continue
    
    # Crear imagen
    img_b64 = crear_imagen_producto(prod["name"], prod["color"])
    
    # Crear producto
    nuevo_prod = call("product.template", "create", [{
        "name": prod["name"],
        "categ_id": cat_pan_id,
        "list_price": prod["price"],
        "type": "product",
        "sale_ok": True,
        "purchase_ok": True,
        "description": prod["desc"],
        "image_1920": img_b64,
    }])
    
    print(f"  [creado] {prod['name']} - ₡{prod['price']:,}")
    conteo += 1

print(f"\n✅ {conteo} productos agregados exitosamente")
print(f"Total de productos en Panadería: {10 + conteo} (incluidos los anteriores)")

# Verificar stock
print("\nVerificando stock de productos...")
prods_count = call("product.template", "search_count", [[]])
print(f"Total de productos en el sistema: {prods_count}")
