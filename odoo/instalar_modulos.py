import xmlrpc.client
import time

url      = "http://localhost:8069"
db       = "pasteleria_db"
username = "andalfaro123@gmail.com"
password = "Gusano1199"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

def call(model, method, args, kwargs={}):
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

# ── Instalar módulos ───────────────────────────────────────────────────────────
modulos = ["sale_management", "stock", "account"]

print("Instalando módulos necesarios...")
for modulo in modulos:
    resultado = call("ir.module.module", "search", [[["name", "=", modulo]]])
    if not resultado:
        print(f"  [no encontrado] {modulo}")
        continue
    mod_id = resultado[0]
    info   = call("ir.module.module", "read", [[mod_id]], {"fields": ["name", "state"]})[0]
    estado = info["state"]
    if estado == "installed":
        print(f"  [ya instalado] {modulo}")
    else:
        print(f"  [instalando]   {modulo} ...")
        call("ir.module.module", "button_immediate_install", [[mod_id]])
        print(f"  [listo]        {modulo}")

print("\nMódulos listos.")
