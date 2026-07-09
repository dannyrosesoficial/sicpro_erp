# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import AccessError


class SolicitudesUsuarios(models.Model):
    _inherit = 'res.users'

    solicitudes_acceso_count = fields.Integer('Solicitudes', compute='_compute_solicitudes_count')

    # Cuenta las solicitudes asociadas al usuario
    def _compute_solicitudes_count(self):
        for each in self:
            solicitudes_ids = self.env['sicpro.modulo.plantilla.acceso'].sudo().search([('codigo_sap', '=', each.pep)])
            each.solicitudes_acceso_count = len(solicitudes_ids)

    # Abre la vista de las solicitudes de los usuarios en el botón inteligente
    def solicitudes_acceso_view(self):
        if self.solicitudes_acceso_count == 0:
            raise AccessError(_("El usuario seleccionado no tiene solicitudes asociadas."))
        else:
            self.ensure_one()
            domain = [('codigo_sap', '=', self.pep)]
            return {
                'name': _('Solicitudes de Accesos'),
                'domain': domain,
                'res_model': 'sicpro.modulo.plantilla.acceso',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
            }

