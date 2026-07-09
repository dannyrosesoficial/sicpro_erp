Python WebDAV Client 3
=========
[![Build Status](https://travis-ci.com/ezhov-evgeny/webdav-client-python-3.svg?branch=develop)](https://travis-ci.com/ezhov-evgeny/webdav-client-python-3)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ezhov-evgeny_webdav-client-python-3&metric=alert_status)](https://sonarcloud.io/dashboard?id=ezhov-evgeny_webdav-client-python-3)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ezhov-evgeny_webdav-client-python-3&metric=coverage)](https://sonarcloud.io/dashboard?id=ezhov-evgeny_webdav-client-python-3)
[![PyPI](https://img.shields.io/pypi/v/webdavclient3)](https://pypi.org/project/webdavclient3/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/webdavclient3)  

Package webdavclient3 based on https://github.com/designerror/webdav-client-python but uses `requests` instead of `PyCURL`.
Proporciona una forma sencilla de trabajar con servidores WebDAV.

Instalación
------------
```bash
$ pip install webdavclient3
```

Uso de la muestra
------------
```python
from webdav3.client import Client
options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "login",
 'webdav_password': "password"
}
client = Client(options)
client.verify = False # Para no verificar los certificados SSL (Default = True)
client.session.proxies(...) # Para configurar el proxy directamente en la sesión (opcional)
client.session.auth(...) # Para configurar la autenticación de proxy directamente en la sesión (opcional)
client.execute_request("mkdir", 'directory_name')
```

Webdav API
==========

Webdav API es un conjunto de acciones webdav de trabajo con almacenamiento en la nube. Este conjunto incluye las siguientes acciones:
`check`, `free`, `info`, `list`, `mkdir`, `clean`, `copy`, `move`, `download`, `upload`, `publish` y `unpublish`.

**Configurar el cliente**

Las claves necesarias para configurar la conexión del cliente con el servidor WebDAV son `webdav_hostname` y `webdav_login`, `webdav_password`.

```python
from webdav3.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "login",
 'webdav_password': "password"
}
client = Client(options)
```

Si su servidor no admite `HEAD` método o hay otras razones para anular los métodos WebDAV predeterminados para acciones use una opción de diccionario `webdav_override_methods`. 
La clave debe estar en la siguiente lista: `check`, `free`, `info`, `list`, `mkdir`, `clean`, `copy`, `move`, `download`, `upload`,
 `publish` y `unpublish`. El valor debe ser un nombre de cadena del método WebDAV, por ejemplo `GET`.
 
```python
from webdav3.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "login",
 'webdav_password': "password",
 'webdav_override_methods': {
            'check': 'GET'
        }

}
client = Client(options)
```

Para configurar un tiempo de espera de solicitudes, puede usar una opción `webdav_timeout` con valor int en segundos, el tiempo de espera se establece de forma predeterminada en 30 segundos.

```python
from webdav3.client import Client

options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "login",
 'webdav_password': "password",
 'webdav_timeout': 30
}
client = Client(options)
```

Cuando se trata de un servidor proxy, debe especificar la configuración para conectarse a través de él.

```python
from webdav3.client import Client
options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "w_login",
 'webdav_password': "w_password", 
 'proxy_hostname':  "http://127.0.0.1:8080",
 'proxy_login':     "p_login",
 'proxy_password':  "p_password"
}
client = Client(options)
```

Si desea utilizar la ruta del certificado al certificado y la clave privada se define de la siguiente manera:

```python
from webdav3.client import Client
options = {
 'webdav_hostname': "https://webdav.server.ru",
 'webdav_login':    "w_login",
 'webdav_password': "w_password",
 'cert_path':       "/etc/ssl/certs/certificate.crt",
 'key_path':        "/etc/ssl/private/certificate.key"
}
client = Client(options)
```

O desea limitar la velocidad o activar el modo detallado:

```python
options = {
 ...
 'recv_speed' : 3000000,
 'send_speed' : 3000000,
 'verbose'    : True
}
client = Client(options)
```

recv_speed: Velocidad límite de velocidad de descarga de datos en bytes por segundo. Predeterminado a velocidad ilimitada.
send_speed: Velocidad límite de velocidad de carga de datos en bytes por segundo. Predeterminado a velocidad ilimitada. 
verbose:    establecer el modo detallado en onoff. Por defecto, el modo detallado está desactivado.

Además, si su servidor no admite `check`, es posible deshabilitarlo:

```python
options = {
 ...
 'disable_check': True
}
client = Client(options)
```

De forma predeterminada, la verificación de recursos remotos está habilitada.

**Synchronous methods**

```python
# Comprobando la existencia del recurso

client.check("dir1/file1")
client.check("dir1")
```

```python
# Obtener información sobre el recurso

client.info("dir1/file1")
client.info("dir1/")
```

```python
# Consultar espacio libre

free_size = client.free()
```

```python
# Obtenga una lista de recursos

files1 = client.list()
files2 = client.list("dir1")
files3 = client.list("dir1", get_info=True) # devuelve una lista de diccionarios con detalles de archivos
```

```python
# Crear el directorio

client.mkdir("dir1/dir2")
```

```python
# Eliminar recurso

client.clean("dir1/dir2")
```

```python
# Copiar recurso

client.copy(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
client.copy(remote_path_from="dir2", remote_path_to="dir3")
```

```python
# Mover recurso

client.move(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
client.move(remote_path_from="dir2", remote_path_to="dir3")
```

```python
# Mover recurso

client.download_sync(remote_path="dir1/file1", local_path="~/Downloads/file1")
client.download_sync(remote_path="dir1/dir2/", local_path="~/Downloads/dir2/")
```

```python
# Descargar recurso

client.upload_sync(remote_path="dir1/file1", local_path="~/Documents/file1")
client.upload_sync(remote_path="dir1/dir2/", local_path="~/Documents/dir2/")
```

```python
# Publica el recurso

link = client.publish("dir1/file1")
link = client.publish("dir2")
```

```python
# Anular la publicación del recurso

client.unpublish("dir1/file1")
client.unpublish("dir2")
```

```python
# Manejo de excepciones

from webdav3.client import WebDavException
try:
...
except WebDavException as exception:
...
```

```python
# Obtén los archivos que faltan

client.pull(remote_directory='dir1', local_directory='~/Documents/dir1')
```

```python
# Enviar archivos faltantes

client.push(remote_directory='dir1', local_directory='~/Documents/dir1')
```

**Métodos asincrónicos**

```python
# Cargar recurso

kwargs = {
 'remote_path': "dir1/file1",
 'local_path':  "~/Downloads/file1",
 'callback':    callback
}
client.download_async(**kwargs)

kwargs = {
 'remote_path': "dir1/dir2/",
 'local_path':  "~/Downloads/dir2/",
 'callback':    callback
}
client.download_async(**kwargs)
```

```python
# Descargar recurso

kwargs = {
 'remote_path': "dir1/file1",
 'local_path':  "~/Downloads/file1",
 'callback':    callback
}
client.upload_async(**kwargs)

kwargs = {
 'remote_path': "dir1/dir2/",
 'local_path':  "~/Downloads/dir2/",
 'callback':    callback
}
client.upload_async(**kwargs)
```

API de recursos
============

API de recursos que utiliza el concepto de programación orientada a objetos que habilita recursos a nivel de nube.

```python
# Consiga un recurso

res1 = client.resource("dir1/file1")
```

```python
# Trabajar con el recurso

res1.rename("file2")
res1.move("dir1/file2")
res1.copy("dir2/file1")
info = res1.info()
res1.read_from(buffer)
res1.read(local_path="~/Documents/file1")
res1.read_async(local_path="~/Documents/file1", callback)
res1.write_to(buffer)
res1.write(local_path="~/Downloads/file1")
res1.write_async(local_path="~/Downloads/file1", callback)
```
