# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import AccessError


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    tareas_count = fields.Integer('Tareas', compute='_compute_tareas_count')
    
    def _compute_tareas_count(self):
        for each in self:
            eventos_ids = self.env['calendar.event'].sudo().search(
                [('attendee_ids.partner_id', '=', each.user_id.partner_id.id)])
            
            each.tareas_count = len(eventos_ids)

    # Abre la vista de las tareas del trabajador en el botón inteligente
    def tareas_trabajador_view(self):
        if self.tareas_count == 0:
            raise AccessError(_("El usuario seleccionado no tiene tareas."))
        else:
            self.ensure_one()
            domain = [('attendee_ids.partner_id', '=', self.user_id.partner_id.id)]
            return {
                'name': _('Tareas'),
                'domain': domain,
                'res_model': 'calendar.event',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id
            }
