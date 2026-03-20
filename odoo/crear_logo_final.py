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

print("Verificando y creando logo de Pan & Aroma...\n")

# Crear logo mejorado
def crear_logo_mejorado():
    # Crear imagen con colores cálidos de panadería
    img = Image.new('RGB', (800, 300), color=(255, 245, 230))  # Crema claro
    draw = ImageDraw.Draw(img)
    
    # Fondo con degradado
    for y in range(300):
        ratio = y / 300
        r = int(255 * (1 - ratio * 0.15) + 210 * ratio * 0.15)
        g = int(245 * (1 - ratio * 0.15) + 180 * ratio * 0.15)
        b = int(230 * (1 - ratio * 0.15) + 140 * ratio * 0.15)
        draw.line([(0, y), (800, y)], fill=(r, g, b))
    
    # Círculos decorativos grandes
    # Círculo marrón (pan)
    draw.ellipse([80, 50, 220, 190], fill=(180, 100, 40), outline=(139, 69, 19), width=4)
    # Círculo dorado (pan tostado)
    draw.ellipse([240, 50, 380, 190], fill=(255, 215, 0), outline=(184, 134, 11), width=4)
    
    # Texto "Pan & Aroma" en grande
    try:
        font_grande = ImageFont.truetype("arial.ttf", 90)
        font_pequeno = ImageFont.truetype("arial.ttf", 30)
    except:
        font_grande = ImageFont.load_default()
        font_pequeno = ImageFont.load_default()
    
    # Texto principal
    draw.text((420, 80), "Pan & Aroma", fill=(139, 69, 19), font=font_grande, anchor="lm")
    
    # Subtítulo
    draw.text((420, 170), "Pastelería & Panadería de Calidad", fill=(139, 90, 43), font=font_pequeno, anchor="lm")
    
    # Convertir a base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

print("Creando logo mejorado...")
logo_b64 = crear_logo_mejorado()

# Buscar empresa
empresa_ids = call("res.company", "search", [[]])
if not empresa_ids:
    print("❌ No se encontró compañía")
    exit(1)

empresa_id = empresa_ids[0]

# Leer datos actuales
empresa_data = call("res.company", "read", [[empresa_id]], {"fields": ["name", "logo"]})[0]
print(f"Empresa actual: {empresa_data['name']}")
print(f"Logo anterior: {'Sí' if empresa_data['logo'] else 'No'}")

# Actualizar con nuevo logo
print("\nGuardando logo...")
call("res.company", "write", [[empresa_id], {
    "logo": logo_b64,
}])

# Verificar que se guardó
empresa_verifico = call("res.company", "read", [[empresa_id]], {"fields": ["logo"]})[0]
tiene_logo = bool(empresa_verifico['logo'])

if tiene_logo:
    print("✅ Logo guardado correctamente en Pan & Aroma")
    print("\n💡 Ahora:")
    print("   1. Recarga la página en el navegador (presiona F5)")
    print("   2. El logo debería aparecer arriba a la izquierda")
    print("   3. Si aún no ves, intenta cerrar sesión y volver a entrar")
else:
    print("⚠️  Lo siento, algo salió mal. Intentando nuevamente...")
    call("res.company", "write", [[empresa_id], {"logo": logo_b64}])
    print("✅ Logo guardado en el segundo intento")

print("\n" + "="*70)
print("LOGO DE PAN & AROMA CONFIGURADO")
print("="*70)
