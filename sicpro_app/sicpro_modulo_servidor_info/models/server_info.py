# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
import logging
import psutil
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self, *args, **kwargs):
        # CAMBIO: Pasar los argumentos al super
        result = super(IrHttp, self).session_info(*args, **kwargs)

        # Seguridad: Solo usuarios con permisos de sistema ven esto
        if not self.env.user.has_group('base.group_system'):
            return result

        try:
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            result['server_stats'] = {
                'cpu': {'usage': psutil.cpu_percent(interval=None),
                    'count': psutil.cpu_count(), },
                'ram': {'total': mem.total, 'used': mem.used,
                    'percent': mem.percent, 'free': mem.free, },
                'disk': {'total': disk.total, 'used': disk.used,
                    'percent': disk.percent, 'free': disk.free, }}
        except Exception as e:
            # Evitamos que un error de psutil rompa el login o la sesión de Odoo
            _logger.error("Error obteniendo estadísticas del servidor: %s", e)

        return result


class ServerInfoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Campo para la vista de configuración
    update_frequency = fields.Selection(string='Frecuencia de actualización',
        selection=[('1000', '1 Sec'), ('2000', '2 Sec'), ('5000', '5 Sec'),
                   ('10000', '10 Sec'), ('30000', '30 Sec'),
                   ('60000', '1 Min')], required=True, default='5000',
        help="Frecuencia con la que el cliente solicita info al servidor")

    def set_values(self):
        """Guardar el valor de forma persistente en ir.config_parameter"""
        super(ServerInfoSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'server_info.update_frequency', self.update_frequency)

    @api.model
    def get_values(self):
        """Recuperar el valor guardado para mostrarlo en la vista de configuración"""
        res = super(ServerInfoSettings, self).get_values()
        res.update(
            update_frequency=self.env['ir.config_parameter'].sudo().get_param(
                'server_info.update_frequency', default='5000'))
        return res