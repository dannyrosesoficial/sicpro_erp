SICPRO ERP
----

SICPRO ERP es un conjunto de aplicaciones empresariales de código abierto basadas en la web.

Repositorio para el desarrollo del proyecto SICPRO.

SICPRO ERP es un conjunto de aplicaciones empresariales de código 
abierto basadas en la web. Las aplicaciones de SICPRO se pueden utilizar como aplicaciones independientes, pero 
también se integran.

Las aplicaciones de SICPRO ERP se pueden usar como aplicaciones independientes, pero también se integran a la 
perfección para que obtenga un <a href='https://sicproerp.dvpe.etecsa.cu/'>ERP de código abierto</a> con todas las 
funciones cuando instala varias aplicaciones.

Ficha Técnica
-------------
Código Abierto, Modular, Personalizable, Multiplataforma, Lanzamiento anual de nuevas versiones, Desarrollado en Python
PostgreSQL como motor de base de datos, Multilenguaje, multimoneda, Ofrece integración con LDAP.


Antecedentes y descripción funcional del sistema
------------------------------------------------
SICPRO ERP es un sistema desarrollado para la gestión integrada de los recursos de la DVPE. Está pensado para la 
integración con distintos software de oficina. Dispone de funcionalidad para la generación de impresos vía PDF, HTML,
y permite exportar datos a otros programas como Open Office o MS Office (Excel, Word).

La arquitectura del sistema es cliente – servidor, sin embargo, cuenta con dos tipos de interfaces de usuario, una 
interfaz web y otra interfaz de escritorio, lo que permite que todos los usuarios trabajen sobre el mismo repositorio 
de datos.

Dispone de interfaces XML-RPC y SOAP y dentro de la construcción misma del software se hace un uso intensivo de flujos
de trabajo (modelo workflow) que se pueden integrar con sus distintos módulos. Es un software multiplataforma y de 
código abierto, funciona sobre LINUX y la interfaz de usuario está construida sobre Gtk. Adicionalmente, este software
permite trabajar vía remota desde una computadora conectada a Internet gracias a un cliente para ambiente Web. 
Emplea a PostgreSQL como sistema manejador de bases de datos y ha sido programado con Python.

Comenzando con SICPRO ERP
-------------------------
Para una instalación estándar, siga las instrucciones de configuración de la documentación del desarrollador.

Requisitos Técnicos
-------------------
Es aconsejable que la instalación se realice sobre un servidor dedicado Linux Server (Ubuntu, CentOS, Debian). 
Se necesita PostgreSQL que es un motor de bases de datos donde el sistema almacenara toda la información. 
Es por esto que para soportar toda la instalación necesitaremos espacio en disco, aproximadamente unos 500Gb 
entre SICPRO ERP, bases de datos, addons, adjuntos, etc. Para el correcto funcionamiento de todo el sistema 
deberíamos de tener al menos 16Gb de memoria RAM y un procesador Intel (64 bits) con 8 núcleos disponibles. 
Para acceder al sistema vamos a necesitar tener instalado un navegador web en la PC.

Instalación del software base
----------------------------
El procedimiento de instalación de SICPRO ERP puede resultar un poco engorroso, por tal sentido a continuación se 
describen los pasos necesarios para realizar una correcta configuración del sistema en general y lograr así una 
eficiente instalación de la aplicación.

    **Actualizar los paquetes del servidor**
    sudo apt-get update && sudo apt-get upgrade

    **Crear Usuario del sistema**
    sudo adduser --system --home=/opt/odoo --group odoo

    **Instalar las siguientes dependencias Python**
    sudo apt-get install -y python3 python3-pip libevent-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev 
    libldap2-dev libssl-dev python3-dev python3-wheel libxslt-dev libzip-dev python3-slugify python3-cachetools 
    python3-setuptools python3-xlrd python3-xlsxwriter libjpeg-dev gdebi libpq-dev build-essential libffi-dev 
    libcurl4-openssl-dev gcc python3-pypdf2 python3-dateutil python3-lxml python3-mako python3-babel python3-pyparsing 
    python3-simplejson python3-tz python3-yaml python3-docutils python3-psutil python3-mock python3-unittest2 
    python3-jinja2 python3-decorator python3-passlib python3-pil python3-psycopg2 python-psycopg2-doc python3-pycurl  
    libtiff5-dev libopenjp2-7-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev 
    python3-venv wget python3-crontab python-pycurl

    sudo pip3 install xlwt num2words PyPDF2 Werkzeug python-dateutil reportlab psycogreen psycopg2-binary 
    httpagentparser webdavclient3 pdfminer pdfminer.six openpyxl setuptools wheel phonenumbers pdfkit vobject 
    icalendar caldav python-gitlab pyinotify watchdog

    sudo apt-get install -y npm
    sudo apt-get install -y node-less
    sudo apt install -f

    **Instalar paquete Wkhtmltopdf**
    sudo apt-get install -y libxrender1 libfontconfig1 libx11-dev libjpeg62 libxtst6 fontconfig xfonts-75dpi 
    xfonts-base 
    sudo apt install wkhtmltopdf

    **Instalar Gestor de Base de Datos PostgreSQL**
    sudo apt-get install postgresql
    sudo su - postgres
    createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo
    #Introducir contraseña
    psql
    ALTER USER odoo WITH SUPERUSER;
    \q
    exit

    **Instalar paquete requeridos de odoo**
    sudo su - odoo -s /bin/bash
    sudo pip3 install -r /opt/odoo/sicpro_erp/odoo/requirements.txt
    exit

    **Verificar archivos de configuración**
    sudo nano /opt/odoo/sicpro_erp/config/odoo/sicpro.conf
    sudo chown odoo: /opt/odoo/sicpro_erp/config/odoo/sicpro.conf
    sudo chmod 640 /opt/odoo/sicpro_erp/config/odoo/sicpro.conf

    **Configurar Servicio**
    sudo cp /opt/odoo/sicpro_erp/config/odoo/sicpro.service /etc/systemd/system/sicpro.service

    **Verificar la configuración**
    sudo nano /etc/systemd/system/sicpro.service
    sudo chmod 755 /etc/systemd/system/sicpro.service
    sudo chown root: /etc/systemd/system/sicpro.service

    **Iniciar Servicios**
    sudo systemctl daemon-reload
    sudo systemctl start sicpro
    sudo systemctl status sicpro
    sudo systemctl enable sicpro

    **Iniciar Navegador**
    http://<Dominio>:8069


Configurar mantenimiento Autovacuum de la base de datos
-------------------------------------------------------
El Autovacuum hace un análisis del estado de cada tabla basándose en las estadísticas de uso, y si considera que debe 
hacerse un VACUUM o un ANALIZE a una tabla, se hace automáticamente.

    sudo nano /etc/postgresql/11/main/postgresql.conf
_Descomentar y modificar los siguientes parámetros:_
`track_counts = on
autovacuum = on                        
log_autovacuum_min_duration = 250       
autovacuum_max_workers = 1            
autovacuum_naptime = 1min             
autovacuum_vacuum_threshold = 128      
autovacuum_analyze_threshold = 256      
autovacuum_vacuum_scale_factor = 0.2   
autovacuum_analyze_scale_factor = 0.1  
autovacuum_freeze_max_age = 200000000  
autovacuum_multixact_freeze_max_age = 400000000        
autovacuum_vacuum_cost_delay = 2ms     
autovacuum_vacuum_cost_limit = -1 `   

    sudo service postgresql restart 

De ser necesario ejecutar un vacuum o un analize de forma manual en la documentación de Mantenimiento están descritos 
los métodos para su ejecución.

Instalación del certificado SSL
------------------------------
Si la instalación se realizó correctamente, ya en este punto debe estar desplegado el servidor de la aplicación, 
utilizando la salida atreves del puerto 8069. Ahora se procede a la instalación del certificado SSL para implementar 
el cifrado de los datos.

El núcleo de Odoo por defecto transmite la información sin cifrar, incluida la de autenticación. Es por ello que un
despliegue seguro de Odoo debe contar con HTTPS, el cual requiere de certificados SSL que a continuación indicaremos 
cómo configurar e instalar.

    **Instalar Nginx**
    sudo apt-get install nginx
    sudo apt install -f

    **Creamos directorio SSL**
    sudo mkdir /etc/nginx/ssl

    **Crear la llave privada**
    sudo openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/sicpro.key -out  /etc/nginx/ssl/sicpro.crt
    sudo chmod 700 /etc/nginx/ssl

    **Copiar archivos de configuración Nginx**
    sudo cp /opt/odoo/sicpro_erp/config/nginx/sicproerp.etecsa.cu.conf /etc/nginx/sites-available/sicproerp.etecsa.cu.conf
    
    **Verifico la configuración**
    sudo nano /etc/nginx/sites-available/sicproerp.etecsa.cu.conf
    sudo ln -s /etc/nginx/sites-available/sicproerp.etecsa.cu.conf /etc/nginx/sites-enabled

Modificar el parámetro del fichero anterior (/etc/nginx/sites- available/ sicproerp.etecsa.cu.conf):
server_name sicproerp.dvpe.etecsa.cu: cambiar por el dominio de la aplicación
Modificar el parámetro del fichero (/etc/nginx/nginx.conf):
Sustituir la línea: 
`ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE `
Por: 
`ssl_protocols TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE `

Dentro del apartado http añadir la directiva:
`http {client_max_body_size 4096M;}`

Edita el siguiente fichero sicpro.conf

    sudo nano /opt/odoo/sicpro_erp/config/odoo/sicpro.conf
    **Descomentar la siguiente línea:**
    proxy_mode = True

Para que los cambios sean efectivos, reiniciar los servicios implicados:
  
    sudo nginx -t
    sudo systemctl restart nginx.service
    sudo systemctl restart sicpro.service

Modificar Firewall para permitir la conexión:

`Permitir conexiones externas hacia puerto 80 y 443 
permitir conexiones a la interfaz local `

Verífica que puedes acceder mediante HTTPS:
https://www.sicproerp.etecsa.cu

OPTIMIZACIÓN DE LA CONFIGURACIÓN
-------------------------------
**Nginx**

    • sudo nano /etc/nginx/nginx.conf

Descomentar las siguientes opciones:

`gzip on;
gzip_vary on;
gzip_proxied any;
gzip_com_level 6;
gzip_buffers 16 8K;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml+rss text/javascript;`

**Agregar a gzip_type** 

`Image/x-icon image/bmp image/png image/jpg image/jpeg image/gif;`

    sudo service nginx reload

**Postgresql**

    cd /etc/postgresql/11/main
    ls
    sudo nano postgresql.conf
    
Modificar los siguientes valores:

`Shared_buffers = *(recomendable 20% de total de la memoria ram)
Effective_cache_size = *(descomentar y el valor recomendado es la mitad de la memoria ram)`

    sudo service postgresql restart
