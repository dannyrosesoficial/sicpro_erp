# -*- coding: utf-8 -*-

from odoo import models, fields


class Municipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipio'
    _order = 'code'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', help='El código del municipio', required=True)
    country_id = fields.Many2one('res.country', string='Pais',
                                 default='base.cu', required=True)
    state_id = fields.Many2one('res.country.state', 'Provincia',
                               domain="[('country_id', '=', country_id)]")
#    zipcode = fields.Many2one('res.city', string='Zip')

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)',
         '¡El código del municipio debe ser único por provincia!')
    ]