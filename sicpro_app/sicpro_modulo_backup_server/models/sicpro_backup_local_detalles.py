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
from urllib.parse import urlencode
from odoo import models, fields
from odoo.exceptions import UserError
from .lib import check_connectivity

_logger = logging.getLogger(__name__)


class SicproBackupLocalDetalles(models.Model):
    _name = 'sicpro.backup.local.detalles'
    _description = "Detalles del proceso de copia de seguridad"
    _order = "id desc"

    name = fields.Char(string="Nombre")
    file_name = fields.Char(string="Nombre del archivo")
    sicpro_backup_local_id = fields.Many2one(
        string="ID del proceso de copia de seguridad",
        comodel_name="sicpro.backup.local")
    file_path = fields.Char(string="Ruta del archivo")
    url = fields.Char(string="Url")
    backup_date_time = fields.Datetime(string="Tiempo de respaldo")
    status = fields.Char(string="Estado")
    message = fields.Char(string="Mensaje")
    backup_location = fields.Selection(
        string="Ubicación de la copia de seguridad",
        related="sicpro_backup_local_id.backup_location",
        help="Servidor donde se almacenará el archivo de respaldo.")

    # Llame mediante el botón de descarga sobre cada registro detallado de la copia de seguridad.
    # Método descargar el archivo zip de copia de seguridad
    def download_db_file(self):
        try:
            backup_file_path = None
            download_url = None
            data = dict()
            if self.backup_location == 'local':
                backup_file_path = self.url
                data = {"path": backup_file_path, "backup_location": 'local'}
            else:
                backup_copy_status = self.get_remote_backup_file()
                if backup_copy_status:
                    backup_file_path = self.sicpro_backup_local_id.remote_server_id.temp_backup_dir + "/" + self.file_name
                    data = {"path": backup_file_path,
                        "backup_location": 'remote'}
                else:
                    raise UserError(
                        "No se puede descargar el archivo de copia de seguridad desde el servidor remoto. Siga los registros para obtener más detalles.")
            download_url = f"/backupfile/download?{urlencode(data)}"
            if self.status == "Success" and os.path.exists(backup_file_path):
                return {'type': 'ir.actions.act_url', 'url': download_url,
                    'target': 'new', }
            else:
                raise UserError("La copia de seguridad no existe.")
        except Exception as e:
            raise UserError(f"Se produjo un error: {e}")

    #  Método para copiar el archivo de copia de seguridad del servidor remoto al servidor principal
    #  Devoluciones:
    #  [Booleano]: Verdadero en caso de que el archivo se copie correctamente o Falso
    def get_remote_backup_file(self):
        try:
            host_server = self.sicpro_backup_local_id.remote_server_id.get_server_details()
            temp_path = self.sicpro_backup_local_id.remote_server_id.temp_backup_dir
            response = check_connectivity.ishostaccessible(host_server)

            if not response.get('status'):
                return False

            ssh_obj = response.get('result')
            sftp = ssh_obj.open_sftp()
            sftp.get(self.url, temp_path + '/' + self.file_name)
            sftp.close()
            _logger.info(
                "======== Archivo de copia de seguridad copiado correctamente en el servidor local. ===========")
            return True
        except Exception as e:
            _logger.info(
                f"======= Excepción al copiar el archivo de copia de seguridad desde el servidor remoto ======= {e} ")
            return False

    def unlink_confirmation(self):
        for rec in self:
            if rec.status == "Success":
                msg = """ <span class="text-warning"><strong>Warning:</strong> Después de eliminar este registro, ya no podrá descargar el archivo de respaldo asociado con este registro. Sin embargo, después de la eliminación, la copia de seguridad seguirá estando en el servidor.
                        ¿Está seguro de que desea eliminar este registro de respaldo?<span>
                      """
                partial_id = self.env['sicpro.backup.eliminacion'].create(
                    {'backup_id': rec.id, 'message': msg})
                return {'type': 'ir.actions.act_window',
                    'name': 'Deletion Confirmation', 'view_mode': 'form',
                    'res_model': 'sicpro.backup.eliminacion',
                    'res_id': partial_id.id, 'target': 'new', }
            else:
                rec.unlink()
