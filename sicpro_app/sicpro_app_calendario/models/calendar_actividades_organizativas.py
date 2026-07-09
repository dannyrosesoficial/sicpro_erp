# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def _default_color():
    return randint(1, 11)


class MeetingActividadesOrganizativas(models.Model):
    _name = 'calendar.actividades.organizativas'
    _description = 'Actividades Organizativas del Calendario'

    name = fields.Char('Actividades', required=True)
    usuarios_ids = fields.Many2many('res.users', string="Usuarios", readonly=False, store=True, )
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    active = fields.Boolean(string='Archivado', required=True, default=True)

    @api.constrains('name')
    def _check_actividades_unico(self):
        uniq = self.env['calendar.actividades.organizativas'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡La actividad introducida ya existe!. "
                                    "Si cree que es un error contacte al administrador"))
