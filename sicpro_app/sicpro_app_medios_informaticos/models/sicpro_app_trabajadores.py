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


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    medios_informaticos_count = fields.Integer(string='Informática',
                                               compute='_compute_medios_count')

    # Cuenta los medios informáticos asociados al trabajador
    def _compute_medios_count(self):
        for each in self:
            medios_ids = self.env[
                'sicpro.app.medios.informaticos'].sudo().search(
                [('trabajador_id', '=', each.id)])

            each.medios_informaticos_count = len(medios_ids)

    # Abre la vista de los medios informáticos de los trabajadores en el botón inteligente
    def medios_trabajador_view(self):
        if self.medios_informaticos_count == 0:
            raise AccessError(
                "El usuario seleccionado no tiene equipos asociados.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            self.ensure_one()
            domain = [('trabajador_id', '=', self.id)]
            return {'name': 'Medios Informáticos', 'domain': domain,
                'res_model': 'sicpro.app.medios.informaticos',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form', 'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id}
