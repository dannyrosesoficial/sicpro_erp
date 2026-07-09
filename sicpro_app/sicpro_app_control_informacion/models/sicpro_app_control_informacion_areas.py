# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class ControlInformacionAreas(models.Model):
    _name = 'sicpro.app.control.informacion.areas'
    _description = 'Áreas para el control de información'

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área asociada', required=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    company_id = fields.Many2one('res.company', string='Proceso', related='name.company_id', store=True)

    @api.constrains('name')
    def _check_area_unica(self):
        uniq = self.env['sicpro.app.control.informacion.areas'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name.id), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El área introducida ya existe!. "
                                    "Si cree que es un error contacte al administrador"))
