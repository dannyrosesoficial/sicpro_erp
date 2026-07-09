# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
from .lib import check_connectivity

_logger = logging.getLogger(__name__)

STATE = [('draft', "Borrador"), ('validated', 'Validado'), ]


class SicproBackupRemoteServer(models.Model):
    _name = 'sicpro.backup.remote.server'
    _description = "Servidor remoto de respaldo"

    name = fields.Char(string="Nombre",
                       help="Nombre del servidor remoto de respaldo")
    sftp_host = fields.Char(string="Host SFTP remoto",
                            help="Host SFTP para establecer conexión con el servidor remoto de respaldo")
    sftp_port = fields.Char(string="Puerto SFTP remoto", default="22",
                            help="Puerto SFTP para establecer conexión con el servidor remoto de respaldo")
    sftp_user = fields.Char(string="Usuario SFTP",
                            help="Usuario SFTP para establecer conexión con el servidor remoto de respaldo")
    sftp_password = fields.Char(string="SFTP Password",
                                help="Contraseña SFTP para establecer la conexión con el servidor remoto de respaldo")
    state = fields.Selection(selection=STATE, string="Estado", default="draft",
                             help="Estado del servidor remoto de respaldo")
    active = fields.Boolean(string="Activo", default=True, index=True)
    temp_backup_dir = fields.Char(
        string="Directorio de copia de seguridad temporal",
        help="La ruta de copia de seguridad temporal donde se almacenan las copias de seguridad antes de pasar al servidor remoto. El directorio de copia de seguridad temporal debe estar presente en el servidor principal junto con los permisos adecuados.")
    def_backup_dir = fields.Char(
        string="Directorio de copia de seguridad remota predeterminado",
        help="La ruta del directorio predeterminado en el servidor remoto donde se almacenarán las copias de seguridad de las instancias del cliente saas. El directorio debe tener los permisos adecuados.")

    # Método para verificar la conexión del Host: llamado por el botón 'Probar conexión'
    def test_host_connection(self):
        for obj in self:
            response = obj.check_host_connected_call()
            if response.get('status'):
                message = self.env['sicpro.backup.mensaje.wizard'].create(
                    {'mensaje': "Conexión exitosa!"})
                action = self.env.ref(
                    'sicpro_modulo_backup_server.action_sicpro_backup_mensaje_wizard').read()[
                    0]
                action['res_id'] = message.id
                return action
            else:
                raise UserError(response.get('message'))

    # Método para llamar al script para verificar la conectividad del host,
    # dictar la respuesta de devolución según el resultado.
    # Llamado desde 'test_host_connection' y 'set_validated'
    def check_host_connected_call(self):
        response = dict(status=True, message='Success')
        host_server = self.get_server_details()
        try:
            response = check_connectivity.ishostaccessible(host_server)
            if response and response.get('status'):
                _logger.info(
                    "======= Conexión del servidor remoto exitosa ======")
                ssh_obj = response.get('result')
                backup_dir = self.def_backup_dir
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
        except Exception as e:
            _logger.info(
                f"------ EXCEPCIÓN AL PROBAR LA CONEXIÓN DEL SERVIDOR REMOTO ---- {e} ------")
            response['status'] = False
            response['message'] = e
        return response

    # Método creado para devolver el valor del servidor host como dict,
    # Llamado desde el método check_host_connected_call en el proceso completo
    @api.model
    def get_server_details(self):
        host_server = dict(host=self.sftp_host, port=self.sftp_port,
            user=self.sftp_user, password=self.sftp_password, )
        return host_server

    def set_validated(self):
        for obj in self:
            response = obj.check_host_connected_call()
            if response.get('status'):
                obj.state = 'validated'
            else:
                raise UserError(response.get('message'))

    def reset_to_draft(self):
        for obj in self:
            bkp_processes = self.env['sicpro.backup.local'].search(
                [('remote_server_id', '=', obj.id),
                 ('backup_location', '=', 'remote'),
                 ('state', 'in', ['confirm', 'running'])])
            if bkp_processes:
                raise UserError(
                    "¡Este servidor remoto tiene algunos procesos de copia de seguridad activos!")
            obj.state = 'draft'

    # Método para ejecutar el comando en el servidor remoto.
    def execute_on_remote_shell(self, ssh_obj, command):
        _logger.info(command)
        response = dict()
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_obj.exec_command(command)
            res = ssh_stdout.readlines()
            _logger.info("execute_on_remote_shell res: %r", res)
            err = ssh_stderr.readlines()
            _logger.info("execute_on_remote_shell err: ")
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
