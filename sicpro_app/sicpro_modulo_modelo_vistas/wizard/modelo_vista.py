# -*- coding: utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import UserError


class ModelosVistas(models.TransientModel):
    _name = 'sicpro.modulo.modelo.vista'
    _description = 'Consulta de vistas de los modelos'

    view_type = fields.Selection(
        selection=[('tree', 'Lista'), ('form', 'Formulario')],
        string='Tipo de vista', default='tree', required=True)
    record_id = fields.Integer(string="Identificador", default="1")
    model_id = fields.Many2one('ir.model', string='Modelo', ondelete='set null')
    model_name = fields.Char(related='model_id.model', string='Nombre del Modelo',
                             readonly=True, store=True)
    filter_domain = fields.Char(string='Aplicar filtro')

    def action_view_model(self):
        if self.view_type == 'form':
            if self.record_id < 1:
                raise UserError(_("ID should be a positive integer"))
            if not self.env[self.model_name].sudo().search(
                    [('id', '=', self.record_id)]):
                raise UserError(_("Enter ID of existing record"))
        domain = self.filter_domain
        if not domain:
            domain = []
        action = {
            'name': self.model_id.name,
            'type': 'ir.actions.act_window',
            'res_model': self.model_name,
            'view_id': False,
            'target': 'main',
            'domain': domain,
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
                'copy': False
            }
        }
        if self.view_type == 'form':
            action.update({
                'res_id': self.record_id,
                'view_mode': 'form',
                'views': [(False, 'form')],
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'views': [(False, 'tree'), (False, 'form')],
            })
        return action
