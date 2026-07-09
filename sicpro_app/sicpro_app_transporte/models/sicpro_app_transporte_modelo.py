# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TransporteModelo(models.Model):
    _name = 'sicpro.app.transporte.modelo'
    _description = 'Modelos del Transporte'
    _order = 'name asc'

    name = fields.Char('Nombre del modelo', required=True)
    brand_id = fields.Many2one('sicpro.app.transporte.modelo.brand',
                               'Fabricante', required=True,
                               help='Manufacturer of the vehicle')
    clase_id = fields.Many2one('sicpro.app.transporte.clase', 'Clase',
                               tracking=True, required=True,
                               help='Clase of the vehicle')
    vendors = fields.Many2many(
        'res.partner', 'sicpro_app_transporte_modelo_rel', 'model_id',
        'partner_id', string='Proveedores')
    manager_id = fields.Many2one('res.users', 'Usuario Manager',
                                 default=lambda self: self.env.uid)
    image_128 = fields.Image(related='brand_id.image_128', readonly=False)

    @api.depends('name', 'brand_id')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.brand_id.name:
                name = record.brand_id.name + '/' + name
            res.append((record.id, name))
        return res
