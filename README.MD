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

> Nota: Necesita crearte un fichero ```.env``` con las siguientes propiedades, para realizar la conexión a una base de datos. Si no tienes alguna puedes usar [Docker mysql] o [XAMPP].
<br>Debes de crear la base de datos para poder utilizar la api, por ejemplo **mi_base_datos**, contraseña **root**, cabe recalcar que esta api usa de host la propiedad DB_HOST_TEST=**localhost**, añadir el puerto al que este expuesto su mysql por defecto suele ser **3306** pero si es diferente cambiarlo.
<br>**SECRET** es un valor hexadecimal que necesita la librería de  jwt para encodear y devolver un token.  Por ejemplo **ab6d9878176a4b50d6ba107f39a9dd64**

|clave|valor|
|--|--|
|DB_NAME|mi_base_datos|
|DB_PASSWORD|root|
|DB_HOST|host|
|DB_HOST_TEST|localhost|
|DB_PORT|3306|
|SECRET|ab6d9878176a4b50d6ba107f39a9dd64|

[Python download]: <https://www.python.org/downloads/>
[Instalando nueva versión python]: <https://www.debugpoint.com/install-python-3-11-ubuntu/>
[Docker mysql]: <https://hub.docker.com/_/mysql>
[XAMPP]: <https://www.apachefriends.org/es/download.html>