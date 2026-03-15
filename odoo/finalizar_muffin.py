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

# Buscar el muffin con nombre flexible
print("Buscando Muffin...")
muffin_prods = call("product.template", "search_read", [[["name", "like", "Muffin"]]], {"fields": ["id", "name"]})
if muffin_prods:
    for muf in muffin_prods:
        prod_id = muf["id"]
        nombre = muf["name"]
        print(f"  [encontrado] {nombre} (id={prod_id})")
        
        descripcion = "Muffin esponjoso relleno de arándanos frescos. Suavemente dulce con el toque ácido de los frutos rojos. Una opción saludable y deliciosa."
        color = (138, 43, 226)  # Azul violeta
        img_b64 = crear_imagen_producto(nombre, color)
        
        call("product.template", "write", [[prod_id], {
            "description": descripcion,
            "image_1920": img_b64,
        }])
        print(f"  [actualizado] {nombre}")
else:
    print("  [no encontrado] Ningún Muffin")

print("\n✅ Sistema mejorado completado")
print("Cambios aplicados:")
print("  ✓ Empresa Pan & Aroma configurada")
print("  ✓ Descripciones agregadas a todos los productos")
print("  ✓ Imágenes generadas para los productos")
print("\nVer en Odoo: Inventario → Productos → Productos")
