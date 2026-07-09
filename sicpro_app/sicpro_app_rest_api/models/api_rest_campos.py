# -*- coding: utf-8 -*-


from odoo import api, fields, models


class ApiRestField(models.Model):
    _name = 'api.rest.field'
    _order = 'sequence'
    _rec_name = 'field_name'
    _description = 'Campos utilizados en el Api Rest'

    sequence = fields.Integer()
    path_id = fields.Many2one(
        'api.rest.path', string='Directorio', required=True, ondelete='cascade')
    model_id = fields.Many2one(
        string='Modelo', related="path_id.model_id", readonly=True)
    field_id = fields.Many2one(
        'ir.model.fields', string='Campo', required=True, ondelete='cascade',
        domain="["
               "('model_id', '=', model_id),"
               "]")
    field_name = fields.Char(
        related="field_id.name", readonly=True)
    description = fields.Char(string='Descripción', )
    force_required = fields.Boolean(
        related="field_id.required", readonly=True)
    required = fields.Boolean(string='Requerido', )
    default_value = fields.Char(string='Valor por Defecto', )

    @api.onchange('field_id')
    def _onchange_field_id(self):
        self.required = self.field_id.required

    @api.onchange('default_value')
    def _onchange_default_value(self):
        if self.default_value:
            self.required = False

    @api.onchange('required')
    def _onchange_required(self):
        if self.default_value:
            self.required = False
