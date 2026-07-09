# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class ModuloHistorial(models.Model):
    _name = 'sicpro.modulo.historial.aplicaciones'
    _description = 'Control de la acciones en las aplicaciones'
    _order = 'create_date desc'

    TYPES = [
        ('install', 'Instalado'),
        ('upgrade', 'Actualizado'),
        ('uninstall', 'Desinstalado'),
    ]

    module_name = fields.Char(required=True, string='Módulo')
    type = fields.Selection(TYPES, required=True, string='Acción')
    user_id = fields.Many2one('res.users', string='Autor', required=True)
    date_event = fields.Datetime(string='Fecha del Evento',
        default=fields.Datetime.now, readonly=True)


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def _button_immediate_function(self, function):
        res = super(IrModuleModule, self)._button_immediate_function(function)
        for module in self:
            try:
                action_type = {'button_install': 'install',
                    'button_upgrade': 'upgrade',
                    'button_uninstall': 'uninstall', }.get(function.__name__)

                if action_type:
                    module_data = module.sudo().read(['name'])[0]
                    module_name_safe = module_data.get('name', 'desconocido')

                    self.env[
                        'sicpro.modulo.historial.aplicaciones'].sudo().create({
                        'module_name': module_name_safe, 'type': action_type,
                        'user_id': self.env.uid, })
            except Exception:
                _logger.exception(
                    'Error registrando historial en SICPRO para un modulo.')
                continue
        return res
