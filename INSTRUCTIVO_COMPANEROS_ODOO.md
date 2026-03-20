# Instructivo rapido para correr el proyecto Odoo en otra computadora (Windows)

Este instructivo sirve para que cualquier companero levante el sistema con la misma base de datos del equipo.

## 1) Instalar herramientas

1. Instalar Docker Desktop.
2. Abrir Docker Desktop y dejarlo encendido.
3. (Opcional) Instalar Git si vas a clonar el repositorio.

## 2) Obtener el proyecto

1. Descargar o clonar el repositorio del proyecto.
2. Abrir una terminal en la carpeta raiz del proyecto.

## 3) Recibir los archivos de respaldo

Deben pasarte estos 2 archivos:

1. `tu_bd.dump`
2. `filestore_tu_bd.tar`

Colocalos en esta carpeta del proyecto:

- `.\respaldo_odoo\`

Al final deberias tener:

- `.\respaldo_odoo\tu_bd.dump`
- `.\respaldo_odoo\filestore_tu_bd.tar`

## 4) Levantar contenedores por primera vez

Ejecutar dentro de la carpeta `odoo`:

```powershell
docker compose up -d
```

## 5) Importar la base de datos y filestore

Volver a la carpeta raiz del proyecto y ejecutar:

```powershell
.\odoo\backup_restore_odoo.ps1 -Mode import -DbName tu_bd -FixedName
```

Nota: `tu_bd` debe ser el nombre real de la base que recibieron.

## 6) Abrir el sistema

1. Ir a `http://localhost:8069`
2. Entrar con la base `tu_bd`.

## 7) Si algo falla

1. Reiniciar servicios:

```powershell
docker compose -f .\odoo\docker-compose.yml restart
```

2. Ver logs de Odoo:

```powershell
docker compose -f .\odoo\docker-compose.yml logs -f web
```

3. Ver logs de Postgres:

```powershell
docker compose -f .\odoo\docker-compose.yml logs -f db
```

## Errores comunes

1. Puerto ocupado (8069): cerrar otro servicio que lo use o cambiar puerto en `docker-compose.yml`.
2. Faltan imagenes/adjuntos: el archivo `filestore_tu_bd.tar` no se copio bien.
3. Error de base inexistente: revisar que `-DbName` coincida con el nombre real de la BD.

---

## Comando unico recomendado para companeros

Si ya tienen Docker encendido y los 2 archivos en `.\respaldo_odoo\`, solo correr:

```powershell
cd .\odoo
docker compose up -d
cd ..
.\odoo\backup_restore_odoo.ps1 -Mode import -DbName tu_bd -FixedName
```
