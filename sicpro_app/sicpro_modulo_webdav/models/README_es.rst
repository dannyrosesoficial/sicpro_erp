Tipos de traducción
Traducción de texto
Texto original
5000 / 5000
Resultados de traducción
webdavclient
============

| PYPI VERSION | | Estado de requisitos | | PullReview Stats |

El Paquete WebDavclient Proporciona Un Trabajo Fácil Y Conveniente Con
Serviénanos WebDAV (Yandex.Drive, Dropbox, Google Drive, Box, 4shared, etc.).
El Paquete INCLUYE LOS SIGUIENTES Componentes: API WEBDAV, API DE RECURSOS Y WDC.

El código fuente del proyecto se puede encontrar.
'AQUÍ <https://github.com/designerror/webdavclient> `__ | github |

Instalación y actualización
========================

**Instalación**

- Linux

.. Código :: bash

    $ sudo apt-get install libxml2-dev libxslt-dev python-dev
    $ sudo apt-get install libcurl4-openssl-dev python-pycurl
    $ sudo easy_install webdavclient

- Mac OS

.. Código :: bash

    $ curl https://bootstrap.pypa.io/ez_setup.py -o - | pitón
    $ Python Setup.py Install --prefix = / opt / setuptools
    $ sudo easy_install webdavclient

**Actualizar**

.. Código :: bash

    $ sudo pip install -u webdavclient

API WEBDAV
==========

WebDAV API es un conjunto de métodos de trabajo webDAV con almacenamiento en la nube. Esto
El juego incluye los siguientes métodos: `` Check``, `` `free``,` `info``,
`` Lista``, `` mkdir``, `` limpio``, `` Copy``, `` Move``, `` descargar``,
`` Sube``, `` Publish`` y `` inhordish``.

** Configuración del cliente **

Las teclas requeridas para configurar la conexión del cliente con WEVDAV-Server son
WebDAV \ _HOSTNAME y WEBDAV \ _LOGIN, WEBDAV, \ _ Contraseña.

.. Código :: Python

    Importar webdav.Client como WC
    opciones = {
     'WebDAV_HOSTNAME': "https://webdav.server.ru",
     'webdav_login': "Iniciar sesión",
     'webdav_password': "contraseña"
    }
    cliente = wc.client (opciones)

Cuando un servidor proxy necesita para especificar la configuración para conectarlo.

.. Código :: Python

    Importar webdav.Client como WC
    opciones = {
     'WebDAV_HOSTNAME': "https://webdav.server.ru",
     'WebDAV_LOGIN': "W_LOGIN",
     'webdav_password': "w_password",
     'proxy_hostname': "http://127.0.0.1:8080",
     'proxy_login': "p_login",
     'proxy_password': "p_password"
    }
    cliente = wc.client (opciones)

Si desea utilizar la ruta del certificado al certificado y la clave privada
se define como sigue:

.. Código :: Python

    Importar webdav.Client como WC
    opciones = {
     'WebDAV_HOSTNAME': "https://webdav.server.ru",
     'WebDAV_LOGIN': "W_LOGIN",
     'webdav_password': "w_password",
     'Cert_Path': "/etc/ssl/certs/certificate.crt",
     'key_path': "/etc/ssl/private/certificate.key"
    }
    cliente = wc.client (opciones)

O desea limitar la velocidad o encender el modo verboso:

.. Código :: Python

    opciones = {
     ...
     'recv_speed': 3000000,
     'Send_Speed': 3000000,
     'verbosa': cierto
    }
    cliente = wc.client (opciones)

| RECV \ _SPEED: velocidad de descarga de datos de límite de velocidad en bytes por segundo.
  Por defecto a la velocidad ilimitada.
| ENVIAR \ _SPEED: Velocidad de carga de datos de límite de velocidad en bytes por segundo.
  Por defecto a la velocidad ilimitada.
| verbose: establecer el modo verboso encender / apagar. Por el modo verboso predeterminado está apagado.

** Métodos síncronos **

.. Código :: Python

    // verificando la existencia del recurso

    Client.Check ("Dir1 / File1")
    Client.Check ("Dir1")

.. Código :: Python

    // obtener información sobre el recurso

    client.info ("dir1 / file1")
    cliente.info ("dir1 /")

.. Código :: Python

    // comprobar espacio libre

    Free_Size = Client.Free ()

.. Código :: Python

    // obtener una lista de recursos

    archivos1 = Client.list ()
    archivos2 = cliente.list ("dir1")

.. Código :: Python

    // Crear el directorio

    cliente.mkdir ("dir1 / dir2")

.. Código :: Python

    // Eliminar recurso

    Client.Clean ("Dir1 / Dir2")

.. Código :: Python

    // copiar recurso

    Client.Copy (remote_path_from = "dir1 / file1", remote_path_to = "dir2 / file1")
    Client.Copy (remote_path_from = "dir2", remote_path_to = "dir3")

.. Código :: Python

    // mover el recurso

    cliente.move (remote_path_from = "dir1 / file1", remote_path_to = "dir2 / file1")
    Client.Move (remote_path_from = "dir2", remote_path_to = "dir3")

.. Código :: Python

    // mover el recurso

    cliente.download_sync (remote_path = "dir1 / file1", local_path = "~ / descargas / file1")
    cliente.download_sync (remote_path = "dir1 / dir2 /", local_path = "~ / descargas / dir2 /")

.. Código :: Python

    // Descargar recurso

    client.upload_sync (remote_path = "dir1 / file1", local_path = "~ / documentos / file1")
    client.upload_sync (remote_path = "dir1 / dir2 /", local_path = "~ / documentos / dir2 /")

.. Código :: Python

    // Publicar el recurso

    link = client.publish ("dir1 / file1")
    link = client.publish ("dir2")

.. Código :: Python

    // un recurso inolvidable

    cliente.unpublish ("dir1 / file1")
    cliente.unpublish ("dir2")

.. Código :: Python

    // Manejo de excepciones

    desde webdav.client Importar WebDavexception
    intentar:
    ...
    Excepto webdavexception como excepción:
    ...

.. Código :: Python

    // obtener los archivos faltantes

    Client.Pull (remote_directory = 'dir1', local_directory = '~ / documentos / dir1')

.. Código :: Python

    // enviar archivos faltantes

    cliente.push (remote_directory = 'dir1', local_directory = '~ / documentos / dir1')

** Métodos asíncronos **

.. Código :: Python

    // cargar los recursos

e
    kwargs = {
     'Remote_Path': "Dir1 / File1",
     'local_path': "~ / descargas / file1",
     'Callback': devolución de llamada
    }
    Client.download_async (** Kwargs)

    kwargs = {
     'Remote_Path': "Dir1 / Dir2 /",
     'local_path': "~ / descargas / dir2 /",
     'Callback': devolución de llamada
    }
    Client.download_async (** Kwargs)

.. Código :: Python

    // Descargar recurso

    kwargs = {
     'Remote_Path': "Dir1 / File1",
     'local_path': "~ / descargas / file1",
     'Callback': devolución de llamada
    }
    Client.upload_async (** kwargs)

    kwargs = {
     'Remote_Path': "Dir1 / Dir2 /",
     'local_path': "~ / descargas / dir2 /",
     'Callback': devolución de llamada
    }
    Client.upload_async (** kwargs)

API de recursos
============

API de recursos utilizando el concepto de OOP que permite el nivel de nube
recursos.

.. Código :: Python

    // obtener un recurso

    res1 = client.resource ("dir1 / file1")

.. Código :: Python

    // trabajar con el recurso

    res1.rename ("file2")
    res1.move ("dir1 / file2")
    res1.copy ("dir2 / file1")
    info = res1.info ()
    res1.read_from (búfer)
    res1.dread (local_path = "~ / documentos / file1")
    res1.read_async (local_path = "~ / documentos / file1", devolución de llamada)
    res1.write_to (buffer)
    res1.write (local_path = "~ / descargas / file1")
    res1.write_async (local_path = "~ / descarga / file1", devolución de llamada)

WDC
===

WDC \ -A Utilidad multiplataforma que proporciona un trabajo conveniente con
WebDAV-servidores a la derecha desde su consola. Además de completo
Implementaciones de métodos de la API de WebDAV, también se agregan contenido de métodos.
Sincronizar directorios locales y remotos.

**Autenticación**

- * Autenticación básica *

.. Código :: bash

   $ WDC Iniciar sesión https://wedbav.server.ru -p http://127.0.0.1:8080
   webdav_login: w_login
   webdav_password: w_password
   proxy_login: p_login
   proxy_password: p_password
   éxito

- Autorizar la solicitud usando OAUTH Token \ *

.. Código :: bash

   $ WDC Login https://wedbav.server.ru -p http://127.0.0.1:8080 - Foto xxxxxxxxxxxxxxxxxx
   proxy_login: p_login
   proxy_password: p_password
   éxito

También hay llaves adicionales `` --root [-R] `',` `--Cert-ruta [-c]` `y
`` -y-Path [-k] ``.

**Utilidad**

.. Código :: bash

    $ WDC Check
    éxito
    $ wdc check file1
    no éxito
    $ wdc gratis
    245234120344
    $ wdc ls dir1
    file1
    ...
    fila
    $ wdc mkdir dir2
    $ wdc copy dir1 / file1 -t dir2 / file1
    $ wdc mudas dir2 / file1 -t dir2 / file2
    $ WDC Descargar Dir1 / File1 -t ~ / descargas / file1
    $ WDC Descargar Dir1 / -T ~ / descargas / DIR1 /
    $ WDC Subir Dir2 / File2 -F ~ / Documentos / File1
    $ WDC Subir Dir2 / -F ~ / Documentos /
    $ wdc Publish di2 / file2
    https://yadi.sk/i/vwttucbucac6k
    $ wdc indecorish dir2 / file2
    $ WDC PULT DIR1 / -T ~ / DOCUMENTOS / DIR1 /
    $ WDC PUSH DIR1 / -F ~ / DOCUMENTOS / DIR1 /
    $ WDC Info Dir1 / File1
    {'nombre': 'File1', 'Modificado': 'Thu, 23 oct 2014 16:16:37 GMT',
    'Tamaño': '3460064', 'creado': '2014-10-23T16: 16: 37Z'}

WebDAV-Server
=============

Los repositorios más populares basados ​​en la nube que apoyan el protocolo.
WebDAV se puede atribuir yandex.drive, Dropbox, Google Drive, Box y
4shared. Acceso a repositorios de datos, operando con acceso a la
Internet. Si es necesario ubicaciones locales y almacenamiento en la nube, puede implementar
su propio servidor webdav.

** WebdAV-Server local **

Para implementar un servidor webDAV local, usando contenedores DOCER con bastante facilidad
y rápido. Para ver un ejemplo de los servidores de despliegue local puede
estar en el proyecto
`WebDAV-Server-Docker <https://github.com/designerror/webdav-server-docker>` __.

** Métodos compatibles **

+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| Servidores | libre | info | Lista | mkdir | limpio | Copia | Mover | Descargar | Subir |
+ ================ + ======== + ======== + ======== + ===== ==== + ========= + ======== + ======== + ============ + ==== ====== + +
| Yandex.disk | \ + | \ + | \ + | \ + | \ + | \ + | \ + | \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| Dropbox | \ - | \ + | \ + | \ + | \ + | \ + | \ + | \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| Google Drive | \ - | \ + | \ + | \ + | \ + | \ - | \ - | \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| Caja | \ + | \ + | \ + | \ + | \ + | \ + | \ + | \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| 4shared | \ - | \ + | \ + | \ + | \ + | \ - | \ - | \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +
| Webdavserver | \ - | \ + | \ + | \ + | \ + | \ - | \ -

Tipos de traducción
Traducción de texto
Texto original
2150 / 5000
Resultados de traducción
| \ + | \ + |
+ ---------------- + -------- + -------- + -------- + ----- ---- + --------- + -------- + -------- + ------------ + ---- ------ +

Los métodos publicar y no publicaron son compatibles solo yandex.disk.

** Configuración de conexiones **

Para trabajar con Cloud Storage Dropbox y Google Drive a través del WebDAV
Protocolo, debe usar un WebDAV-Server Dropdav y DAV-BLEGE,
respectivamente.

Una lista de configuraciones para servidores webDAV:

.. Código :: YAML

    Webdav-servidores:
     - yandex
         Nombre de host: https://webdav.yandex.ru
         Iniciar sesión: #login_for_yandex
         Contraseña: #pass_for_yandex
     - Dropbox
         nombre de host: https://dav.dropdav.com
         Iniciar sesión: #Login_For Dropdav
         Contraseña: #pass_for_dropdav
     - Google
         Nombre de host: https://dav-pocket.appspot.com
         raíz: docso
         Inicio de sesión: # login_for_dav-bolsillo
         Contraseña: # pass_for_dav-bolsillo
     - caja
         nombre de host: https://dav.box.com
         raíz: dav
         Iniciar sesión: #login_for_box
         Contraseña: #pass_for_box
     - 4shared
         Nombre de host: https://webdav.4shared.com
         Iniciar sesión: # LOGIN_FOR_4SHARED
         Contraseña: # pass_for_4shared

Autocompletación
===============

Para MacOS, o sistemas de Unix más antiguos, necesita actualizar Bash.

.. Código :: bash

    $ BREW INSTALAR BASH
    $ chs
    $ BREW INSTALAR BASH-FINICIÓN

Autocompletión se puede habilitar globalmente

.. Código :: bash

    $ sudo activate-global-python-argomplete

o localmente

.. Código :: bash

    # .bashrc
    eval "$ (Registrar-Python-Argomplete WDC)"

.. | Versión PYPI | Imagen :: https://badge.fury.io/py/webdavclient.svg
   : objetivo: http://badge.fury.io/py/webdavclient
.. | Estado de requisitos | Imagen :: https://requires.io/github/designerror/webdav-client-python/requirements.svg?branch=master&style=flat
   : objetivo: https://requires.io/github/designerror/webdav-client-python/requirements/?branch=master&style=flat
.. | PullReview Stats | Imagen :: https://www.pullreview.com/github/designerror/webdavclient/badges/master.svg?
   : objetivo: https://www.pullreview.com/github/designerror/webdavclient/reviews/master
.. | GitHub | Imagen :: https://github.com/favicon.ico
Más información sobre este texto de origen
Para obtener más información sobre la traducción, se necesita el texto de origen
Enviar comentarios
Paneles laterales
Límite de 5.000 caracteres. Utiliza las flechas para seguir traduciendo.


