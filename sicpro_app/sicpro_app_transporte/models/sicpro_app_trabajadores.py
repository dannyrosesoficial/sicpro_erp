# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models
from odoo.exceptions import AccessError


class TransporteTrabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    transporte_count = fields.Integer(string='Vehículo',
                                      compute='_compute_vehiculos_count')

    # Cuenta los vehículos asociados al trabajador
    def _compute_vehiculos_count(self):
        for each in self:
            transporte_ids = self.env[
                'sicpro.app.transporte.general'].sudo().search(
                [('chofer_trabajador_id', '=', each.id)])
            each.transporte_count = len(transporte_ids)

    # Abre la vista de los vehículos de los trabajadores
    # en el botón inteligente
    def transporte_trabajador_view(self):
        if self.transporte_count == 0:
            raise AccessError(
                "El usuario seleccionado no tiene vehículo asociado.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            self.ensure_one()
            domain = [('chofer_trabajador_id', '=', self.id)]
            return {'name': 'Vehículos', 'domain': domain,
                'res_model': 'sicpro.app.transporte.general',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form', 'limit': 80,
                'context': "{'default_chofer_trabajador_id': %s}" % self.id}
