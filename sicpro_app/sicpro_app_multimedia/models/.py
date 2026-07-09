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

    vivienda_materiales_count = fields.Integer(string='Materiales',
                                               compute='_compute_materiales_count')

    # Cuenta los materiales entregados al trabajador
    def _compute_materiales_count(self):
        for each in self:
            materiales_ids = self.env[
                'sicpro.app.vivienda.trabajador.productos'].sudo().search(
                [('solicitud_id.trabajador_id', '=', each.id),
                 ("estado", "in", ['aprobado', 'entregado'])])
            each.vivienda_materiales_count = len(materiales_ids)

    # Abre la vista del trabajador en el programa de la vivienda
    def vivienda_materiales_trabajador_view(self):
        if self.vivienda_materiales_count == 0:
            raise AccessError(
                "El Trabajador seleccionado no tiene entregas en el programa de la vivienda.\n\n" + MSG_SOPORTE_SICPRO)
        else:
            self.ensure_one()
            domain = [('trabajador_id', '=', self.id)]
            return {'name': 'Programa de la vivienda', 'domain': domain,
                'res_model': 'sicpro.app.vivienda.trabajador',
                'type': 'ir.actions.act_window', 'view_id': False,
                'view_mode': 'list,form', 'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id}
