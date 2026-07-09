# -*- coding: utf-8 -*-


from os import remove, path
from webdav3.client import Client
from odoo import models, fields, _
from odoo.exceptions import Warning
import zipfile


class SicproAdministracionNubeAplicaciones(models.Model):
    _name = 'sicpro.app.administracion.nube.aplicaciones'
    _description = 'Gestión de las aplicaciones en la nube'

    name = fields.Char(string='Aplicación', required=False)
    directorio_remoto = fields.Char('Directorio Externo',
                                    default='SICPRO_STORE', required=True)
    directorio_local = fields.Char('Directorio Local',
                                   default='/opt/odoo/sicpro_erp/app/',
                                   required=True)
    host = fields.Char('Servidor Webdav', required=True)
    usuario = fields.Char('Usuario', required=True)
    password = fields.Char('Contraseña', required=True)

    # Prueba de conexión al servidor models
    def test_webdav_connection(self, context=None):
        self.ensure_one()

        # Comprueba si hay éxito o no y escribe mensajes.
        message_title = ""
        message_content = ""
        error = ""
        has_failed = False

        for rec in self:
            ip_host = rec.host
            username_login = rec.usuario
            password_login = rec.password
            remote_path = rec.directorio_remoto

            options = {'webdav_hostname': ip_host,
                       'webdav_login': username_login,
                       'webdav_password': password_login, }
            client = Client(options)
            client.verify = False

            # Conéctese con un servidor externo a través de WEBDAV, para estar
            # seguros de que todo funciona.
            try:
                chequeo = client.check(remote_path)
                capacidad = round(client.free() / 1048576)
                message_title = _(
                    "Prueba de conexión exitosa!\n¡Todo parece configurado "
                    "correctamente para copias de seguridad de WEBDAV!\nSu "
                    "capacidad actual es: " + str(capacidad) + " MB")
            except Exception as e:
                error += str(e)
                raise Warning(
                    'Hubo un problema al conectarse al WEBDAV remoto: %s',
                    str(e))

        has_failed = True
        message_title = _("¡Prueba de conexión fallida!")
        message_content += _("Esto es lo que obtuvimos en su lugar:\n")

        if has_failed:
            raise Warning(
                message_title + '\n\n' + message_content + "%s" % str(error))
        else:
            raise Warning(message_title + '\n\n' + message_content)

    # sincronizar archivo remoto con el local
    def sincronizar(self):
        ip_host = self.host
        username_login = self.usuario
        password_login = self.password
        remote_path = self.directorio_remoto

        options = {'webdav_hostname': ip_host, 'webdav_login': username_login,
                   'webdav_password': password_login, }
        client = Client(options)
        client.verify = False

        # valor = client.free()
        dir_remoto = str(self.directorio_remoto + "/" + self.name)
        dir_local = str(self.directorio_local + "/" + self.name)

        client.download_sync(remote_path=dir_remoto, local_path=dir_local)

        # raise Warning(valor)

        directorio_zip = dir_local
        directorio_descomprimir = self.directorio_local
        password = None

        # creo el objeto zip
        archivo_zip = zipfile.ZipFile(directorio_zip, "r")

        # verificar el contenido del archivo .zip
        # raise Warning(archivo_zip.namelist())

        try:
            # descomprimo el archivo .zip
            archivo_zip.extractall(pwd=password, path=directorio_descomprimir)
            # elimino el archivo después de descomprimir
            if path.exists(directorio_zip):
                remove(directorio_zip)
        except OSError as error:
            raise Warning(
                '¡Error al descomprimir o eliminar el archivo .zip! Error: %s',
                str(error))
            pass
        archivo_zip.close()

    # verificar contenido de archivo .zip local
    def verifica_zip_local(self):
        dir_local = str(self.directorio_local + "/" + self.name)
        directorio_zip = dir_local

        # creo el objeto zip
        archivo_zip = zipfile.ZipFile(directorio_zip, "r")

        # verificar el contenido del archivo .zip
        raise Warning(archivo_zip.namelist())

    # verificar contenido de archivo remoto
    def verifica_zip_remoto(self):
        dir_remoto = str(self.directorio_remoto + "/" + self.name)

        ip_host = self.host
        username_login = self.usuario
        password_login = self.password

        options = {'webdav_hostname': ip_host, 'webdav_login': username_login,
                   'webdav_password': password_login, }
        client = Client(options)
        client.verify = False

        # verificar el contenido del archivo .zip
        archivo_zip = client.check(dir_remoto)

        raise Warning(archivo_zip)
