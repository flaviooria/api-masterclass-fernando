# Masterclass I.E.S Fernando III with FastApi

## Requerimientos
**Descarga de Python**
[Python download] Sitio oficial para descarga de python versiones mayores a +10.* 
- Si ya cuentas con alguna versión de python (Para usuarios linux/mac)
*[Instalando nueva versión python]*

- Para usuarios de windows, tendrían que des-instalar el anterior e instalar la nueva versión que se hayan descargado.
```sh
python -m  venv  env
```
### En la terminal de linux/mac
```sh
source env/bin/activate
pip install -r requirements.txt
```
### En la terminal de windows
```sh
env/Scripts/activate
pip install -r requirements.txt
```
### Ejecutar proyecto
```sh
uvicorn main:app --reload --port 3000
```

> Nota: Necesita crearte un fichero ```.env``` con las siguientes propiedades.

|clave|valor|
|--|--|
|DB_NAME|base_datos_nombre|
|DB_PASSWORD|contraseña|
|DB_HOST|host|
|DB_HOST_TEST|host|
|DB_PORT|puerto|
|SECRET|hash|

[Python download]: https://www.python.org/downloads/
[Instalando nueva versión python]: https://www.debugpoint.com/install-python-3-11-ubuntu/