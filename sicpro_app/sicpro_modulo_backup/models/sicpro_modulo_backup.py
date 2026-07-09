# -*- coding: utf-8 -*-

from os import remove, path, listdir, stat, makedirs
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import shutil
import json
import tempfile
from webdav3.client import Client
import psutil
from odoo import models, fields, api, tools, _
from odoo.exceptions import Warning, AccessDenied, UserError
import odoo

import logging

_logger = logging.getLogger(__name__)

try:
    import paramiko
except ImportError:
    raise ImportError(
        'Este módulo necesita paramiko para escribir automáticamente copias de'
        ' seguridad en el FTP a través de SFTP. '
        'Instale paramiko en el sistema. (sudo pip3 install paramiko)')


class DbBackup(models.Model):
    _name = 'sicpro.modulo.backup'
    _description = 'Configura las salvas automáticas del sistema'

    def _get_db_name(self):
        dbName = self._cr.dbname
        return dbName

    # Columnas para la configuración del servidor local
    host = fields.Char('Host', required=True, default='localhost')
    port = fields.Char('Puerto', required=True, default=8069)
    name = fields.Char('Base de Datos', required=True, default=_get_db_name)
    folder = fields.Char('Directorio backup', required='True',
                         default='/odoo/backups')
    backup_type = fields.Selection([('zip', 'Zip'), ('dump', 'Dump')],
                                   'Tipo de copia', required=True,
                                   default='zip')
    autoremove = fields.Boolean('Auto eliminar')
    days_to_keep = fields.Integer('Eliminar después de x días', default=30,
                                  required=True)

    # Columnas para servidor externo (SFTP)
    sftp_write = fields.Boolean('Escribir en un servidor externo con sftp')
    sftp_path = fields.Char('Ruta del servidor externo SFTP')
    sftp_host = fields.Char('Servidor SFTP de dirección IP')
    sftp_port = fields.Integer('Puerto SFTP', default=22)
    sftp_user = fields.Char('Nombre de usuario Servidor SFTP')
    sftp_password = fields.Char('Servidor SFTP de usuario de contraseña')
    days_to_keep_sftp = fields.Integer('Eliminar SFTP después de x días',
                                       default=30)
    send_mail_sftp_fail = fields.Boolean('Enviar correo electrónico si hay '
                                         'error en la copia de seguridad')
    email_to_notify = fields.Char('Email Sftp para notificar')

    # Columnas para servidor externo (Webdav)
    webdav_write = fields.Boolean('Escribir en un servidor externo con Webdav')
    webdav_path = fields.Char('Ruta del servidor externo WEBDAV',
                              default='SICPRO_BACKUP')
    webdav_host = fields.Char('Servidor Webdav o dirección IP')
    webdav_user = fields.Char('Usuario del Servidor Webdav')
    webdav_password = fields.Char('Contraseña del servidor Webdav')
    webdav_autoremove = fields.Boolean('Auto eliminar Webdav')
    webdav_to_keep = fields.Integer('Eliminar Webdav después de x días',
                                    default=10)
    webdav_email_to_notify = fields.Char('Email Webdav para notificar')

    # datos del archivo .zip
    archivo = fields.Char('archivo', required=False)
    capacidad_local = fields.Char('Capacidad local', required=False)
    capacidad_remoto = fields.Char('Capacidad remoto', required=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    # Prueba de conexión al servidor models
    def test_webdav_connection(self, context=None):
        self.ensure_one()

        # Comprueba si hay éxito o no y escribe mensajes.
        message_title = ""
        message_content = ""
        error = ""
        has_failed = False

        for rec in self:
            ip_host = rec.webdav_host
            username_login = rec.webdav_user
            password_login = rec.webdav_password
            remote_path = rec.webdav_path

            options = {'webdav_hostname': ip_host,
                       'webdav_login': username_login,
                       'webdav_password': password_login, }
            client = Client(options)
            client.verify = False

            # Conéctese con un servidor externo a través de WEBDAV, para estar
            # seguros de que todo funciona.
            try:
                chequeo = client.check(remote_path)
                capacidad = round(client.free() / 1048576, 2)
                message_title = _(
                    "Prueba de conexión exitosa!\n¡Todo parece configurado "
                    "correctamente para copias de seguridad de WEBDAV!\nSu "
                    "capacidad actual es: " + str(capacidad) + " MB")
            except Exception as e:
                _logger.critical(
                    'Hubo un problema al conectarse al WEBDAV remoto: %s',
                    str(e))
                error += str(e)
                has_failed = True
                message_title = _("¡Prueba de conexión fallida!")

                message_content += _("Esto es lo que obtuvimos en su lugar:\n")

        if has_failed:
            raise Warning(
                message_title + '\n\n' + message_content + "%s" % str(error))
        else:
            raise Warning(message_title + '\n\n' + message_content)

    # Prueba de conexión al servidor sftp
    def test_sftp_connection(self, context=None):
        self.ensure_one()

        # Comprueba si hay éxito o no y escribe mensajes.
        message_title = ""
        message_content = ""
        error = ""
        has_failed = False

        for rec in self:
            ip_host = rec.sftp_host
            port_host = rec.sftp_port
            username_login = rec.sftp_user
            password_login = rec.sftp_password

            # Conéctese con un servidor externo a través de SFTP, para estar seguros de que todo funciona.
            try:
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(ip_host, port_host, username_login, password_login,
                          timeout=10)
                sftp = s.open_sftp()
                sftp.close()
                message_title = _(
                    "Prueba de conexión exitosa!\n¡Todo parece configurado correctamente para copias de seguridad de FTP!")
            except Exception as e:
                _logger.critical(
                    'Hubo un problema al conectarse al ftp remoto: %s', str(e))
                error += str(e)
                has_failed = True
                message_title = _("¡Prueba de conexión fallida!")
                if len(rec.sftp_host) < 8:
                    message_content += "\nSu dirección IP parece ser demasiado corta.\n"
                message_content += _("Esto es lo que obtuvimos en su lugar:\n")
            finally:
                if s:
                    s.close()

        if has_failed:
            raise Warning(
                message_title + '\n\n' + message_content + "%s" % str(error))
        else:
            raise Warning(message_title + '\n\n' + message_content)

    @api.model
    def ejecutar_backup(self):
        conf_ids = self.search([])
        for rec in conf_ids:
            try:
                if not path.isdir(rec.folder):
                    makedirs(rec.folder)
            except:
                raise
            # Create name for dumpfile.
            bkp_file = '%s_%s.%s' % (
                time.strftime('%d_%m_%Y_%H_%M_%S'), rec.name, rec.backup_type)
            file_path = path.join(rec.folder, bkp_file)
            fp = open(file_path, 'wb')
            rec.archivo = bkp_file
            # Indicamos la ruta de origen.
            disk_usage = psutil.disk_usage(rec.folder)

            cl_total = round(disk_usage.total / 1024 ** 3, 2)
            cl_libre = round(disk_usage.free / 1024 ** 3, 2)
            cl_usado = round(disk_usage.used / 1024 ** 3, 2)
            cl_porcentaje = disk_usage.percent
            capacidad_local = "Usado: " + str(
                cl_usado) + " GB " + ", Libre: " + str(
                cl_libre) + " GB " + ", Total: " + str(
                cl_total) + " GB " + ", Estado: " + str(
                cl_porcentaje) + " %"
            rec.capacidad_local = capacidad_local
            try:
                # try to backup database and write it away
                fp = open(file_path, 'wb')
                self._take_dump(rec.name, fp, 'sicpro.modulo.backup',
                                rec.backup_type)
                fp.close()
            except Exception as error:
                _logger.debug(
                    "No se pudo hacer una copia de seguridad de la base de "
                    "datos %s. Contraseña de administrador de base de datos "
                    "incorrecta para el servidor que se ejecuta en "
                    "https://%s:%s" % (rec.name, rec.host, rec.port))
                _logger.debug("Exact error from the exception: %s", str(error))
                continue

            # guardo el archivo en el registro de la BD para la eliminación.
            vals = {'name': bkp_file}
            self.env['sicpro.modulo.backup.archivos'].create(vals)
            ###################################################################

            # Compruebe si el usuario quiere escribir en SFTP o no.
            if rec.sftp_write is True:
                try:
                    # Store all values in variables
                    dir = rec.folder
                    path_to_write_to = rec.sftp_path
                    ip_host = rec.sftp_host
                    port_host = rec.sftp_port
                    username_login = rec.sftp_user
                    password_login = rec.sftp_password
                    _logger.debug('ruta remota sftp: %s', path_to_write_to)

                    try:
                        s = paramiko.SSHClient()
                        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        s.connect(ip_host, port_host, username_login,
                                  password_login, timeout=20)
                        sftp = s.open_sftp()
                    except Exception as error:
                        _logger.critical(
                            '¡Error al conectarse al servidor remoto! Error: %s',
                            str(error))

                    try:
                        sftp.chdir(path_to_write_to)
                    except IOError:
                        # Create directory and subdirs if they do not exist.
                        current_directory = ''
                        for dirElement in path_to_write_to.split('/'):
                            current_directory += dirElement + '/'
                            try:
                                sftp.chdir(current_directory)
                            except:
                                _logger.info(
                                    '(Parte del) camino hizon\'t existe. Creándolo ahora en %s',
                                    current_directory)
                                # Make directory and then navigate into it
                                sftp.mkdir(current_directory, 777)
                                sftp.chdir(current_directory)
                                pass
                    sftp.chdir(path_to_write_to)
                    # Loop over all files in the directory.
                    for f in listdir(dir):
                        if rec.name in f:
                            fullpath = path.join(dir, f)
                            if path.isfile(fullpath):
                                try:
                                    sftp.stat(path.join(path_to_write_to, f))
                                    _logger.debug(
                                        'Archivo %s ya existe en el servidor FTP remoto ------ omitido',
                                        fullpath)
                                # This means the file does not exist (remote) yet!
                                except IOError:
                                    try:
                                        sftp.put(fullpath,
                                                 path.join(path_to_write_to,
                                                           f))
                                        _logger.info(
                                            'Copiando archivo % s------ éxito',
                                            fullpath)
                                    except Exception as err:
                                        _logger.critical(
                                            'No pudimos\'t escribir el archivo en el servidor remoto. Error: %s',
                                            str(err))

                    # Navigate in to the correct folder.
                    sftp.chdir(path_to_write_to)

                    _logger.debug("Comprobando archivos caducados")
                    # Recorra todos los archivos del directorio desde las copias de seguridad.
                    # Comprobaremos la fecha de creación de cada copia de seguridad.
                    for file in sftp.listdir(path_to_write_to):
                        if rec.name in file:
                            # Obtén el camino completo
                            fullpath = path.join(path_to_write_to, file)
                            # Obtenga la marca de tiempo del archivo en el servidor externo
                            timestamp = sftp.stat(fullpath).st_mtime
                            createtime = datetime.datetime.fromtimestamp(
                                timestamp)
                            now = datetime.datetime.now()
                            delta = now - createtime
                            # Si el archivo es anterior a days_to_keep_sftp (los días para mantener que el usuario completó
                            # en el formulario de Odoo se eliminará.
                            if delta.days >= rec.days_to_keep_sftp:
                                # Only delete files, no directories!
                                if ".dump" in file or '.zip' in file:
                                    _logger.info(
                                        "Eliminar un archivo demasiado antiguo de los servidores SFTP: %s",
                                        file)
                                    sftp.unlink(file)
                    # Cierre la sesión SFTP.
                    sftp.close()
                    s.close()
                except Exception as e:
                    try:
                        sftp.close()
                        s.close()
                    except:
                        pass
                    _logger.error(
                        '¡Excepción! Pudimosn\'t realizar una copia de seguridad en el servidor FTP. Esto es lo que recuperamos '
                        'instead: %s', str(e))
                    # En este punto, la copia de seguridad SFTP falló. Ahora comprobaremos si el usuario quiere
                    # una notificación por correo electrónico sobre esto.
                    if rec.send_mail_sftp_fail:
                        try:
                            ir_mail_server = self.env['ir.mail_server'].search(
                                [], order='sequence asc', limit=1)
                            message = "¡Querido!,\n\nLa copia de seguridad del servidor " + rec.host + " (IP: " + rec.sftp_host + ") ha fallado. Por favor revise los siguientes detalles:\n\nIServidor SFTP de dirección IP: " + rec.sftp_host + "\nNombre de usuario: " + rec.sftp_user + "\n\nError de detalles: " + tools.ustr(
                                e) + "\n\nAtentamente"
                            catch_all_domain = self.env[
                                "ir.config_parameter"].sudo().get_param(
                                "mail.catchall.domain")
                            response_mail = "sicpro_modulo_backup@%s" % catch_all_domain if catch_all_domain else self.env.user.partner_id.email
                            msg = ir_mail_server.build_email(response_mail, [
                                rec.email_to_notify],
                                                             "Copia de seguridad de " + rec.host + "(" + rec.sftp_host + ") ha fallado",
                                                             message)
                            ir_mail_server.send_email(msg)
                        except Exception:
                            pass
            ###################################################################

            # Compruebe si el usuario quiere escribir en WEBDAV o no.
            if rec.webdav_write is True:
                try:
                    _logger.debug('ruta remota models: %s', rec.webdav_path)

                    options = {'webdav_hostname': rec.webdav_host,
                               'webdav_login': rec.webdav_user,
                               'webdav_password': rec.webdav_password,
                               'disable_check': True,
                               'verbose': True}

                    client = Client(options)
                    client.verify = False
                    # Verifico que exista el directorio sino lo creo
                    if not client.check(rec.webdav_path):
                        client.mkdir(rec.webdav_path)

                    # devuelvo la capacidad restante del servidor remoto
                    client = Client(options)
                    client.verify = False
                    capacidad = round(client.free(), 2)
                    rec.capacidad_remoto = str(capacidad)

                    client = Client(options)
                    client.verify = False
                    # envío el documento a la nube
                    dir_remoto = str(rec.webdav_path + "/" + bkp_file)
                    client.upload_sync(remote_path=dir_remoto,
                                       local_path=file_path)

                    # envío el correo a los seguidores del registro
                    local_context = self.env.context.copy()
                    template = self.env.ref(
                        'sicpro_modulo_backup.backup_nuevo_backup')
                    template.with_context(local_context).send_mail(self.id,
                                                                   force_send=True)

                except Exception as error:
                    # Aqui va notificaciónes del error del envio fallido
                    _logger.critical(
                        '¡Error al enviar el archivo al servidor remoto! Error: %s',
                        str(error))
                    #######################################################

    def _take_dump(self, db_name, stream, model, backup_format='zip'):
        """Volcar la base de datos `db` en un objeto similar a un archivo` stream`
        si el stream es None devuelve un objeto de archivo con el volcado """

        cron_user_id = self.env.ref(
            'sicpro_modulo_backup.backup_crear').user_id.id
        if self._name != 'sicpro.modulo.backup' or cron_user_id != self.env.user.id:
            _logger.error('Operación de base de datos no autorizada. '
                          'Las copias de seguridad solo deben estar disponibles '
                          'desde el trabajo cron.')
            raise AccessDenied()

        _logger.info('DUMP DB: %s format %s', db_name, backup_format)

        cmd = ['pg_dump', '--no-owner']
        cmd.append(db_name)

        if backup_format == 'zip':
            with tempfile.TemporaryDirectory() as dump_dir:
                filestore = odoo.tools.config.filestore(db_name)
                if path.exists(filestore):
                    shutil.copytree(filestore,
                                    path.join(dump_dir, 'filestore'))
                with open(path.join(dump_dir, 'manifest.json'), 'w') as fh:
                    db = odoo.sql_db.db_connect(db_name)
                    with db.cursor() as cr:
                        json.dump(self._dump_db_manifest(cr), fh, indent=4)
                cmd.insert(-1, '--file=' + path.join(dump_dir, 'dump.sql'))
                odoo.tools.exec_pg_command(*cmd)
                if stream:
                    odoo.tools.osutil.zip_dir(dump_dir, stream,
                                              include_dir=False,
                                              fnct_sort=lambda
                                                  file_name: file_name != 'dump.sql')
                else:
                    t = tempfile.TemporaryFile()
                    odoo.tools.osutil.zip_dir(dump_dir, t, include_dir=False,
                                              fnct_sort=lambda
                                                  file_name: file_name != 'dump.sql')
                    t.seek(0)
                    return t
        else:
            cmd.insert(-1, '--format=c')
            stdin, stdout = odoo.tools.exec_pg_command_pipe(*cmd)
            if stream:
                shutil.copyfileobj(stdout, stream)
            else:
                return stdout

    def _dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100,
                                      100)
        cr.execute(
            "SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
        modules = dict(cr.fetchall())
        manifest = {'odoo_dump': '1', 'db_name': cr.dbname,
                    'version': odoo.release.version,
                    'version_info': odoo.release.version_info,
                    'major_version': odoo.release.major_version,
                    'pg_version': pg_version, 'modules': modules, }
        return manifest

    @api.model
    def eliminar_backup(self):
        conf_ids = self.search([])
        for rec in conf_ids:
            # Elimine todos los archivos antiguos (en el servidor local) en
            # caso de que esté configurado.
            if rec.autoremove:
                directorio = rec.folder
                dias = rec.days_to_keep
                delta = datetime.now() - relativedelta(days=dias)

                data = self.env['sicpro.modulo.backup.archivos'].search(
                    ['&', ('active_local', '=', True),
                     ('fecha_subida', '<=', delta)])

                # Verifico que exista el archivo y elimino
                for file in data:
                    archivo = str(directorio) + "/" + str(file.name)
                    data.active_local = False
                    # verifico que el archivo existe
                    if path.exists(archivo):
                        remove(archivo)
                        # envio notificación
            ###################################################################

            # Elimine los archivos antiguos (en el servidor remoto models)
            # en caso de que esté configurado.
            if rec.webdav_autoremove:
                try:
                    dias_webdav = rec.webdav_to_keep
                    delta = datetime.now() - relativedelta(days=dias_webdav)
                    data = self.env['sicpro.modulo.backup.archivos'].search(
                        ['&', ('active_webdav', '=', True),
                         ('fecha_subida', '<=', delta)])
                    _logger.debug('ruta remota models: %s', rec.webdav_path)

                    # Verifico que exista el archivo y elimino
                    options = {'webdav_hostname': rec.webdav_host,
                               'webdav_login': rec.webdav_user,
                               'webdav_password': rec.webdav_password, }
                    client = Client(options)
                    client.verify = False

                    # verifico que exista el archivo remoto
                    archivo_remoto = rec.webdav_path + "/" + str(data.name)
                    if client.check(archivo_remoto):
                        client = Client(options)
                        client.verify = False
                        client.clean(archivo_remoto)
                        data.active_webdav = False

                        # envío el correo a los seguidores del registro
                        local_context = self.env.context.copy()
                        template = self.env.ref(
                            'sicpro_modulo_backup.backup_eliminado_backup')
                        template.with_context(local_context).send_mail(self.id,
                                                                       force_send=True)

                except Exception as error:
                    # Aqui va notificaciónes del error del envio fallido
                    _logger.critical(
                        '¡Error al eliminar el archivo del servidor remoto! Error: %s',
                        str(error))

    def prueba3(self):
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_modulo_backup.backup_nuevo_backup')
        template.with_context(local_context).send_mail(self.id, force_send=True)
