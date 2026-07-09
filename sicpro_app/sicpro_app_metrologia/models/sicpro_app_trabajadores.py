# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import AccessError


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    equipamiento_count = fields.Integer(string='Equipos',
                                        compute='_compute_equipment_count')

    # Cuenta los equipos asociados al trabajador
    def _compute_equipment_count(self):
        for each in self:
            equipos_ids = self.env[
                'sicpro.app.metrologia.equipos'].sudo().search(
                [('trabajador_id', '=', each.id)])
            each.equipamiento_count = len(equipos_ids)

    # Abre la vista de los equipos de los trabajadores en el botón inteligente
    def equipos_trabajador_view(self):
        if self.equipamiento_count == 0:
            raise AccessError(
                "El usuario seleccionado no tiene equipos asociados.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            self.ensure_one()
            domain = [('trabajador_id', '=', self.id)]
            return {'name': 'Equipos', 'domain': domain,
                'res_model': 'sicpro.app.metrologia.equipos',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form', 'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id}
