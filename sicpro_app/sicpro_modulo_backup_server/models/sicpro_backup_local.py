# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models, tools
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.addons.sicpro_modulo_backup_server.models.lib import \
    manage_backup_crons
from odoo.exceptions import UserError
from odoo.tools.config import config

_logger = logging.getLogger(__name__)

LOCATION = [('local', 'Local'), ('remote', 'Servidor Remoto'), ]
CYCLE = [('half_day', 'Dos veces al dia'), ('daily', 'Diario'),
         ('weekly', 'Semanal'), ('monthly', 'Mensual'), ('yearly', 'Anual'), ]
STATE = [('draft', 'Borrador'), ('confirm', 'Confirmado'),
         ('running', 'En ejecución'), ('cancel', 'Cancelada')]


class SicproBackupLocal(models.Model):
    _name = "sicpro.backup.local"
    _description = "Proceso de copia de seguridad"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    def _default_db_name(self):
        return self.env.cr.dbname

    name = fields.Char(string="Nombre", default='Copia',
                       help="Nombre para mostrar del proceso de copia de seguridad.")
    frequency = fields.Integer(string="Frequency", default=1,
                               help="Frecuencia para realizar copias de seguridad de la base de datos.")
    frequency_cycle = fields.Selection(selection=CYCLE,
                                       string="Ciclo de frecuencia",
                                       help="Seleccione el ciclo de frecuencia de la copia de seguridad de la base de datos.",
                                       tracking=True)
    storage_path = fields.Char(string="Ruta de almacenamiento",
                               help="La ruta del directorio donde se almacenarán los archivos de respaldo en el servidor.",
                               tracking=True)
    backup_location = fields.Selection(selection=LOCATION,
                                       string="Ubicación de la copia de seguridad",
                                       default="local",
                                       help="Servidor donde se almacenará el archivo de respaldo.")
    retention = fields.Integer(
        string="Recuento de retención de copias de seguridad", default=7,
        help="Recuento de copias de seguridad recientes que se conservarán después de eliminar las copias de seguridad antiguas en el servidor.")
    db_name = fields.Char(string="Nombre de la base de datos",
                          default=_default_db_name,
                          help="Base de datos utilizada para la creación de la copia de seguridad..",
                          tracking=True)
    backup_starting_time = fields.Datetime(
        string="Hora de inicio de la copia de seguridad",
        help="Establecer fecha y hora de inicio de la copia de seguridad de la base de datos.")
    state = fields.Selection(string="Estado", selection=STATE, default='draft',
                             help="Estado actual del proceso de copia de seguridad.")
    update_requested = fields.Boolean(string="Actualización solicitada",
                                      default=False,
                                      help="Comprobado si se solicita alguna copia de seguridad en la copia de seguridad de la base de datos..")
    master_pass = fields.Char(string="Contraseña maestra")
    backup_details_ids = fields.One2many(
        comodel_name="sicpro.backup.local.detalles",
        inverse_name="sicpro_backup_local_id",
        string="Detalles de la copia de seguridad",
        help="Detalles de las copias de seguridad de la base de datos que se han creado..")
    backup_format = fields.Selection(
        [('zip', 'zip (incluye almacén de archivos)'),
         ('dump', 'pg_dump formato personalizado (sin almacén de archivos)')],
        string="Formato de copia de seguridad", default="zip",
        help="Seleccione el formato de archivo del archivo de copia de seguridad de datos.",
        tracking=True)
    enable_retention = fields.Boolean(
        string="Eliminar copias de seguridad antiguas", default=False,
        help="Marque si desea eliminar las copias de seguridad antiguas almacenadas en el servidor.")
    remote_server_id = fields.Many2one(
        comodel_name="sicpro.backup.remote.server",
        string="Servidor remoto de respaldo",
        domain=[('state', '=', 'validated')])

    # Método para cambiar el valor de la frecuencia dos veces al día.
    @api.onchange('frequency_cycle')
    def change_frequency_value(self):
        if self.frequency_cycle == 'half_day':
            self.frequency = 2
        else:
            self.frequency = 1

    # Método para comprobar los servidores remotos validados.
    @api.onchange('backup_location')
    def change_backup_location(self):
        if self.backup_location == 'remote':
            backup_servers = self.env[
                'sicpro.backup.remote.server'].sudo().search(
                [('state', '=', 'validated')])
            if not backup_servers:
                raise UserError(
                    "No se encontraron servidores remotos validados. "
                    "Primero configure un servidor remoto!!")
        self.remote_server_id = None

    # Método para comprobar el valor del campo de retención.
    @api.constrains('retention')
    def check_retention_value(self):
        if self.enable_retention:
            if self.retention < 1:
                raise UserError(
                    "El recuento de retención de copias de seguridad debe ser al menos 1.\n\n" + MSG_SOPORTE_SICPRO)

    # Llamado por el método create_backup_request, definido a continuación
    # Método para llamar al script para crear un cron para administrar las copias de seguridad,
    # llamar al script requiere pocos argumentos, algunos se pasan en este método y se preparan a continuación
    def call_backup_script(self, master_pass=None, port_number=None, url=None,
                           db_user=None, db_password=None, kwargs={}):
        try:
            db_user = db_user or config.get('db_user')
            db_password = db_password or config.get('db_password')
            module_path = tools.misc.file_path('sicpro_modulo_backup_server')
            module_path = module_path + '/models/lib/saas_client_backup.py'
            backup_format = self.backup_format or "zip"
            backup_location = self.backup_location
            res = None
            if hasattr(self,
                       '_call_%s_backup_script' % backup_location):  ## Si desea actualizar el diccionario, puede definir esta función _call_{backup_location}_backup_script
                res = getattr(self,
                              '_call_%s_backup_script' % backup_location)(
                    master_pass, port_number, url, db_user, db_password,
                    backup_format, kwargs)
            return res
        except Exception as e:
            body = "¡No se puede crear un cron de respaldo! ERROR: {}".format(
                e)
            self.message_post(body=body,
                              subject="Excepción de creación de copia de seguridad")
            _logger.error(
                f"------Error al crear una solicitud de copia de seguridad----{e}--------------")

    # Llamado por el método call_backup_script, definido anteriormente
    # Método para llamar al script para crear un cron para administrar las copias de seguridad,
    # llamar al script requiere pocos argumentos, algunos se pasan en este método y se preparan a continuación
    def _call_local_backup_script(self, master_pass=None, port_number=None,
                                  url=None, db_user=None, db_password=None,
                                  backup_format="zip", kwargs={}):
        res = None
        if self.backup_location == "local":
            module_path = tools.misc.file_path('sicpro_modulo_backup_server')
            module_path = module_path + '/models/lib/saas_client_backup.py'
            res = manage_backup_crons.add_cron(master_pass=master_pass,
                                               main_db=self._cr.dbname,
                                               db_name=self.db_name,
                                               backup_location=self.backup_location,
                                               frequency=self.frequency,
                                               frequency_cycle=self.frequency_cycle,
                                               storage_path=self.storage_path,
                                               url=url, db_user=db_user,
                                               db_password=db_password,
                                               process_id=self.id,
                                               module_path=module_path,
                                               backup_format=backup_format,
                                               backup_starting_time=self.backup_starting_time,
                                               kwargs=kwargs)

        if res.get('success'):
            self.state = 'running'
        else:
            body = "No se puede crear un cron de respaldo. Error: {}".format(
                res.get('msg'))
            self.message_post(body=body,
                              subject="Excepción de creación de copia de seguridad")
        return res

    # Llamado por el método call_backup_script, definido anteriormente
    # Método para llamar al script para crear un cron para administrar copias de seguridad de bases de datos remotas,
    # llamar al script requiere pocos argumentos, algunos se pasan en este método y se preparan a continuación
    def _call_remote_backup_script(self, master_pass=None, port_number=None,
                                   url=None, db_user=None, db_password=None,
                                   backup_format="zip", kwargs=dict()):
        res = None
        if self.backup_location == "remote":
            module_path = tools.misc.file_path('sicpro_modulo_backup_server')
            module_path = module_path + '/models/lib/saas_client_backup.py'
            kwargs.update(rhost=self.remote_server_id.sftp_host,
                          rport=self.remote_server_id.sftp_port,
                          ruser=self.remote_server_id.sftp_user,
                          rpass=self.remote_server_id.sftp_password,
                          temp_bkp_path=self.remote_server_id.temp_backup_dir, )
            res = manage_backup_crons.add_cron(master_pass=master_pass,
                                               main_db=self._cr.dbname,
                                               db_name=self.db_name,
                                               backup_location=self.backup_location,
                                               frequency=self.frequency,
                                               frequency_cycle=self.frequency_cycle,
                                               storage_path=self.storage_path,
                                               url=url, db_user=db_user,
                                               db_password=db_password,
                                               process_id=self.id,
                                               module_path=module_path,
                                               backup_format=backup_format,
                                               backup_starting_time=self.backup_starting_time,
                                               kwargs=kwargs)

        if res.get('success'):
            self.state = 'running'
        else:
            body = "No se puede crear un cron de respaldo. Error: {}".format(
                res.get('msg'))
            self.message_post(body=body,
                              subject="Excepción de creación de copia de seguridad")
        return res

    # Método llamado desde Cron,
    # Método llamado el script para actualizar el cron ya creado.
    def update_backup_request(self):
        res = manage_backup_crons.update_cron(db_name=self.db_name,
                                              process_id=str(self.id),
                                              frequency=self.frequency,
                                              frequency_cycle=self.frequency_cycle)
        if res.get('success'):
            self.update_requested = False

    # Método llamado el método para llamar al script crone
    # Agregue 'master_passwd' en el archivo de configuración de odoo
    def create_backup_request(self):
        master_pass = config.get('admin_passwd')
        if master_pass:
            url = "localhost:" + str(config.get('http_port', '8069'))
            return self.call_backup_script(master_pass=master_pass, url=url)
        else:
            body = "No se puede crear un cron de respaldo: la contraseña maestra (master_passwd) no está configurada en el archivo de configuración"
            self.message_post(body=body,
                              subject="Excepción de creación de copia de seguridad")
            _logger.error(
                "------Error al crear la solicitud de copia de seguridad: la contraseña maestra (master_passwd) no está configurada en el archivo de configuración!!----------------")

    # Llamado por el botón sobre la página del proceso de copia de seguridad,
    # Para cancelar el registro del proceso de copia de seguridad y llamar al script de eliminación cron
    def remove_attached_cron(self):
        if self.state == 'running':
            res = manage_backup_crons.remove_cron(db_name=self.db_name,
                                                  process_id=str(self.id),
                                                  frequency=self.frequency,
                                                  frequency_cycle=self.frequency_cycle)
        else:
            res = dict(success=True)
        if res.get('success'):
            self.state = 'cancel'
            return res

    # Método crone para llamar funciones ya sea para crear un nuevo cron o para actualizar uno existente
    @api.model
    def ignite_backup_server_crone(self):
        current_time = fields.Datetime.now()
        processes = self.env['sicpro.backup.local'].sudo().search(
            [('backup_starting_time', '<=', current_time),
             ('state', '=', 'confirm')])
        for process in processes:
            process.create_backup_request()

        upt_processes = self.env['sicpro.backup.local'].sudo().search(
            [('backup_starting_time', '<=', current_time),
             ('state', '=', 'running'), ('update_requested', '=', True)])
        for upt_process in upt_processes:
            if upt_process.update_requested:
                upt_process.update_backup_request()

        # Funcionalidad para enviar correos electrónicos al administrador en caso de copias de seguridad fallidas..
        confirmed_processes = self.env['sicpro.backup.local'].sudo().search(
            [('state', '=', 'running')])
        time_now = fields.Datetime.now()
        yesterday = time_now - relativedelta(days=1)
        failed_backups = confirmed_processes.mapped(
            'backup_details_ids').filtered(lambda
            p: p.status == 'Failure' and p.backup_date_time >= yesterday)
        if failed_backups:
            _logger.info("========== copias de seguridad fallidas ======= %r",
                         failed_backups)
            self.send_backup_failure_mail(failed_backups)

    # Método para enumerar los administradores de odoo.
    def get_odoo_admins(self):
        admin_list = []
        users = self.env['res.users'].sudo().search([])
        for user in users:
            if user.has_group('base.group_system'):
                admin_list.append(user.partner_id.id)
        return admin_list

    # Método para enviar el correo de falla de la copia de seguridad a los usuarios administradores.
    def send_backup_failure_mail(self, failed_backups):
        for obj in failed_backups:
            admin_list = self.get_odoo_admins()
            template = self.env.ref(
                'sicpro_modulo_backup_server.backup_failure_template')
            email_values = {"recipient_ids": admin_list}
            mail_id = template.send_mail(obj.id, force_send=True,
                                         email_values=email_values)
            current_mail = self.env['mail.mail'].browse(mail_id)
            current_mail.send()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sicpro.backup.local')
            res = super(SicproBackupLocal, self).create(vals)
        return res

    def write(self, vals):
        now = fields.Datetime.now()
        if self.state not in ['draft', 'cancel',
                              'confirm'] and self.backup_starting_time and self.backup_starting_time <= now and not vals.get(
            'update_requested') == False:
            vals['update_requested'] = True
        return super(SicproBackupLocal, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state not in ['draft', 'cancel', 'confirm']:
                raise UserError(
                    "No se permite eliminar respaldos que no estén en borrador, cancelados o confirmados.")
        return super(SicproBackupLocal, self).unlink()

    # Llamado por el botón Confirmar sobre el registro del proceso de copia de seguridad
    def confirm_process(self):
        if self.state == 'draft':
            # Genera un error si la contraseña maestra no está configurada en el archivo de configuración de odoo
            if not config.get('admin_passwd', False):
                raise UserError(
                    "¡El parámetro de contraseña maestra (master_passwd) no está configurado en el archivo de configuración de Odoo!!")

            # Creando el archivo de registro de respaldo si no existe
            if not os.path.exists(manage_backup_crons.LOG_FILE_PATH):
                fp = open(manage_backup_crons.LOG_FILE_PATH, 'x')
                fp.close()

            if self.backup_location == 'remote':
                self.validate_remote_backup()
            self.state = "confirm"

    # Llamado por el botón Cancelar sobre el registro del proceso de copia de seguridad.
    def cancel_process(self):
        if self.state in ['draft', 'confirm']:
            self.state = "cancel"

    # Método cron para llamar funciones para eliminar el archivo de copia de seguridad de los
    # procesos de copia de seguridad
    @api.model
    def remove_old_backups(self):
        processes = self.env['sicpro.backup.local'].sudo().search(
            [('state', '=', 'running'), ('enable_retention', '=', True)])
        for rec in processes:
            details_ids = rec.backup_details_ids.filtered(
                lambda d: d.status == "Success").sorted(key=lambda p: p.id)
            if details_ids:
                end_index = len(details_ids) - rec.retention
                if end_index > 0:
                    updated_details_ids = details_ids[:end_index]
                    rec.remove_backup_files(updated_details_ids)

    # Método para comprobar si el archivo de copia de seguridad existe y, si existe, eliminarlo.
    #             Además, actualiza el estado y el mensaje de los detalles del proceso de respaldo.
    #
    #             Argumentos:
    #                 bkp_details_ids ([objeto]): [todos los identificadores del proceso de copia de seguridad cuyo
    #                 archivo de copia de seguridad debe eliminarse].
    def remove_backup_files(self, bkp_details_ids):
        try:
            msg = None
            for bkp in bkp_details_ids:
                backup_location = self.backup_location
                if hasattr(self,
                           '_remove_%s_backup_files' % backup_location):  ##Si desea actualizar el diccionario, puede definir esta función _remove_{backup_location}_backup_files
                    msg = getattr(self,
                                  '_remove_%s_backup_files' % backup_location)(
                        bkp)
                _logger.info("---- %r -- ", msg)
            return True
        except Exception as e:
            _logger.error(
                "Error de eliminación de copia de seguridad de la base de datos: " + str(
                    e))
            return False

    # Método para verificar si el archivo de respaldo existe en el servidor principal,
    # y si existe, elimine ese archivo de copia de seguridad.
    def _remove_local_backup_files(self, bkp_details_id):
        msg = None
        if os.path.exists(bkp_details_id.url):
            res = os.remove(bkp_details_id.url)
            msg = 'La copia de seguridad de la base de datos se realizó correctamente en ' + datetime.now().strftime(
                "%m-%d-%Y-%H:%M:%S") + " después de la retención."
            bkp_details_id.message = msg
            bkp_details_id.status = "Dropped"
        else:
            msg = "El archivo de copia de seguridad de la base de datos no existe."
            bkp_details_id.message = msg
            bkp_details_id.status = "Failure"

        return msg

    # Método para comprobar si el archivo de copia de seguridad existe en el servidor de copia de seguridad remoto,
    # y si existe, elimine ese archivo de copia de seguridad.
    def _remove_remote_backup_files(self, bkp_details_id):
        msg = None
        ssh_obj = self.login_remote()
        if self.check_remote_backup_existance(ssh_obj, bkp_details_id.url):
            sftp = ssh_obj.open_sftp()
            sftp.remove(bkp_details_id.url)
            sftp.close()
            msg = 'La copia de seguridad de la base de datos se realizó correctamente en ' + datetime.now().strftime(
                "%m-%d-%Y-%H:%M:%S") + " después de la retención desde el servidor remoto."
            bkp_details_id.message = msg
            bkp_details_id.status = "Dropped"
        else:
            msg = "El archivo de copia de seguridad de la base de datos no existe en el servidor remoto."
            bkp_details_id.message = msg
            bkp_details_id.status = "Failure"

        return msg

    # Método para iniciar sesión en el servidor de respaldo remoto usando SSH.
    #
    #         Devoluciones:
    #             [Objeto]: [Devuelve el objeto SSh si se conecta correctamente al servidor remoto.]
    def login_remote(self):
        try:
            import paramiko
            ssh_obj = paramiko.SSHClient()
            ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_obj.connect(hostname=self.remote_server_id.sftp_host,
                            username=self.remote_server_id.sftp_user,
                            password=self.remote_server_id.sftp_password,
                            port=self.remote_server_id.sftp_port)
            return ssh_obj
        except ImportError:
            raise UserError(
                "Módulo paramiko no encontrado. Instálelo usando pip: pip3 install paramiko")
        except Exception as e:
            _logger.info(
                f"==== Excepción al conectarse al servidor remoto ==== {e} ===")
            return False

    def test_host_connection(self):
        if self.remote_server_id:
            response = self.validate_remote_backup()
            if response:
                message = self.env['sicpro.backup.mensaje.wizard'].create(
                    {'message': "Conexión exitosa!"})
                action = self.env.ref(
                    'sicpro_modulo_backup_server.action_sicpro_backup_mensaje_wizard').read()[
                    0]
                action['res_id'] = message.id
                return action

    # Método para validar el proceso de respaldo remoto.
    # Comprueba la conexión al servidor remoto junto con la existencia de copia de seguridad.
    #  ruta de almacenamiento en el servidor remoto.
    def validate_remote_backup(self):
        ssh_obj = self.login_remote()
        if ssh_obj:
            backup_dir = self.storage_path
            cmd = "ls %s" % (backup_dir)
            check_path = self.execute_on_remote_shell(ssh_obj, cmd)
            if check_path and not check_path.get('status'):
                raise UserError(
                    f"La ruta de almacenamiento no existe en el servidor remoto. Cree la ruta de respaldo mencionada en el servidor remoto. Error: {check_path.get('message')}")

            cmd = f"touch {backup_dir}/test.txt"
            create_file = self.execute_on_remote_shell(ssh_obj, cmd)
            if create_file and not create_file.get('status'):
                raise UserError(
                    f"El usuario ssh mencionado no tiene derechos para crear archivos. Proporcione los permisos necesarios en la ruta de copia de seguridad predeterminada. Error: {create_file.get('message')}")
            else:
                cmd = f"rm {backup_dir}/test.txt"
                delete_file = self.execute_on_remote_shell(ssh_obj, cmd)
                if delete_file and delete_file.get('status'):
                    _logger.info(
                        "======== Permisos del directorio de respaldo verificados exitosamente =========")

        else:
            raise UserError("No se pudo conectar al servidor remoto.")

        return True

    # Método para comprobar la existencia del archivo de copia de seguridad en el servidor remoto.
    #             Argumentos:
    #                 ssh_obj ([objeto]): [Objeto SSH del servidor remoto.]
    #                 bkp_path ([objeto]): [Ruta del archivo de copia de seguridad en el servidor remoto.]
    def check_remote_backup_existance(self, ssh_obj, bkp_path):
        cmd = "ls -f %s" % (bkp_path)
        check_path = self.execute_on_remote_shell(ssh_obj, cmd)
        if check_path and not check_path.get('status'):
            _logger.error(
                f"-----------Archivo de copia de seguridad de la base de datos '{bkp_path}' no existe en el servidor remoto.--------")
            return False
        return True

    # Método para ejecutar el comando en el servidor remoto.
    def execute_on_remote_shell(self, ssh_obj, command):
        _logger.info(command)
        response = dict()
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_obj.exec_command(command)
            # _logger.info(ssh_stdout.readlines())
            res = ssh_stdout.readlines()
            _logger.info("execute_on_remote_shell res: %r", res)
            _logger.info("execute_on_remote_shell err: ")
            err = ssh_stderr.readlines()
            _logger.info(err)
            if err:
                response['status'] = False
                response['message'] = err
                return response
            response['status'] = True
            response['result'] = res
            return response
        except Exception as e:
            _logger.info("+++ERROR++", command)
            _logger.info("++++++++++ERROR++++", e)
            response['status'] = False
            response['message'] = e
            return response
