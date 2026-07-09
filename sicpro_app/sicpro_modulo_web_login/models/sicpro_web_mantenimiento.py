# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class SicproMantenimiento(models.Model):
    _name = 'sicpro.modulo.web.mantenimiento'
    _description = 'Control de Mantenimiento SICPRO'

    name = fields.Char(string='Referencia',
                       default='Configuración de Mantenimiento SICPRO')
    active_maintenance = fields.Boolean(string='Sistema en Mantenimiento',
                                        default=False)
    estimated_time = fields.Char(string='Tiempo Estimado (HH:MM:SS)',
                                 default='00:30:00')
    maintenance_start_date = fields.Datetime(string='Fecha de Inicio',
                                             help="Se actualiza al activar el mantenimiento")

    maintenance_password = fields.Char(string='Contraseña Maestra')
    confirm_maintenance_password = fields.Char(string='Confirmar Contraseña')

    @api.model_create_multi
    def create(self, vals_list):
        # Validar si ya existe un registro antes de crear nuevos
        if self.search_count([]) >= 1:
            raise ValidationError(
                "Ya existe una configuración activa.\n\n" + MSG_SOPORTE_SICPRO)

        for vals in vals_list:
            # Si el usuario activa el mantenimiento, asignamos la fecha de inicio
            if vals.get('active_maintenance'):
                vals['maintenance_start_date'] = fields.Datetime.now()

            # Validamos contraseñas en la creación si el mantenimiento está activo
            p1 = vals.get('maintenance_password')
            p2 = vals.get('confirm_maintenance_password')
            if vals.get('active_maintenance') and p1 != p2:
                raise ValidationError(
                    "Las contraseñas de mantenimiento no coinciden.")

        return super(SicproMantenimiento, self).create(vals_list)

    def write(self, vals):
        # Si el usuario activa el mantenimiento ahora, guardamos la fecha actual
        if vals.get('active_maintenance') is True:
            vals['maintenance_start_date'] = fields.Datetime.now()

        # Validación de contraseñas durante la edición
        # Obtenemos valores nuevos o los que ya tiene el registro si no se modifican
        for record in self:
            p1 = vals.get('maintenance_password', record.maintenance_password)
            p2 = vals.get('confirm_maintenance_password',
                          record.confirm_maintenance_password)
            active = vals.get('active_maintenance', record.active_maintenance)

            if active and p1 != p2:
                raise ValidationError(
                    "Las contraseñas de mantenimiento no coinciden.")

        return super(SicproMantenimiento, self).write(vals)

    @api.constrains('maintenance_password', 'confirm_maintenance_password')
    def _check_passwords(self):
        for record in self:
            if record.active_maintenance and record.maintenance_password != record.confirm_maintenance_password:
                raise ValidationError(
                    "Las contraseñas de mantenimiento no coinciden.\n\n" + MSG_SOPORTE_SICPRO)
