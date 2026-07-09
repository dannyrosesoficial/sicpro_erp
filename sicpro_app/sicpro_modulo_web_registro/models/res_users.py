# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models
from odoo.exceptions import UserError


class SolicitudesUsuarios(models.Model):
    _inherit = 'res.users'

    solicitudes_acceso_count = fields.Integer(string='Solicitudes',
                                              compute='_compute_solicitudes_count')

    def _compute_solicitudes_count(self):
        # Filtramos usuarios que tengan el campo 'pep' para evitar búsquedas innecesarias
        usuarios_con_pep = self.filtered('pep')
        pep_list = usuarios_con_pep.mapped('pep')

        counts = {}
        if pep_list:
            result = self.env[
                'sicpro.modulo.solicitud.acceso'].sudo()._read_group(
                [('codigo_sap', 'in', pep_list)], groupby=['codigo_sap'],
                aggregates=['__count'])

            # El resultado de _read_group en Odoo 19 devuelve tuplas (valor_grupo, total)
            counts = {codigo_sap: count for codigo_sap, count in result}

        for user in self:
            # Asignamos el conteo basado en el diccionario o 0 si no existe
            user.solicitudes_acceso_count = counts.get(user.pep, 0)

    def solicitudes_acceso_view(self):
        self.ensure_one()
        if self.solicitudes_acceso_count == 0:
            raise UserError(
                "El usuario %s no tiene solicitudes de acceso registradas." % (
                        self.name or ''))

        return {'name': 'Solicitudes de Accesos',
                'type': 'ir.actions.act_window',
                'res_model': 'sicpro.modulo.solicitud.acceso',
                'view_mode': 'list,form',
                'domain': [('codigo_sap', '=', self.pep)],
                'context': {'default_codigo_sap': self.pep},
                'target': 'current', }
