# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import AccessError


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    equipamiento_count = fields.Integer('Equipos', compute='_compute_equipment_count')

    # Cuenta los equipos asociados al trabajador
    def _compute_equipment_count(self):
        for each in self:
            equipos_ids = self.env['sicpro.app.metrologia.equipos'].sudo().search([('trabajador_id', '=', each.id)])
            each.equipamiento_count = len(equipos_ids)

    # Abre la vista de los equipos de los trabajadores en el botón inteligente
    def equipos_trabajador_view(self):
        if self.equipamiento_count == 0:
            raise AccessError(_("El usuario seleccionado no tiene equipos asociados."))
        else:
            self.ensure_one()
            domain = [('trabajador_id', '=', self.id)]
            return {
                'name': _('Equipos'),
                'domain': domain,
                'res_model': 'sicpro.app.metrologia.equipos',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id
            }

