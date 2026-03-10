import xmlrpc.client
url = "http://localhost:8069"
db  = "pasteleria_db"
uid = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common").authenticate(db, "andalfaro123@gmail.com", "Gusano1199", {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
prods = models.execute_kw(db, uid, "Gusano1199", "product.template", "search_read", [[]], {"fields": ["name","type","categ_id","active"], "limit": 30})
print(f"Total productos encontrados: {len(prods)}")
for p in prods:
    print(f"  - {p['name']} | tipo={p['type']} | activo={p['active']} | cat={p['categ_id']}")
