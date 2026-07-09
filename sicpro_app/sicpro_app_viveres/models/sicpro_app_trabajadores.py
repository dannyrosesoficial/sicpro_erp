# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import AccessError


class Trabajadores(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    cantidad_productos_entregados = fields.Integer('Víveres', compute='_compute_productos_count')

    # Cuenta la cantidad de productos entregados al trabajador
    def _compute_productos_count(self):
        for each in self:
            productos_ids = self.env['sicpro.app.viveres.trabajadores.entregas'].sudo().search(
                [('trabajador_id', '=', each.id)])

            each.cantidad_productos_entregados = len(productos_ids)

    # Abre la vista de las entregas de los trabajadores en el botón inteligente
    def entregas_trabajador_view(self):
        if self.cantidad_productos_entregados == 0:
            raise AccessError(_("Al trabajador seleccionado no se le han entregado productos."))
        else:
            self.ensure_one()
            domain = [('trabajador_id', '=', self.id)]
            return {
                'name': _('Víveres'),
                'domain': domain,
                'res_model': 'sicpro.app.viveres.trabajadores.entregas',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'limit': 80,
                'context': "{'default_trabajador_id': %s}" % self.id
            }
