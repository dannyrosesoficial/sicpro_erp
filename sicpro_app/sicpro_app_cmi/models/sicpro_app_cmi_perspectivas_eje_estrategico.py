# -*- coding: utf-8 -*-


from random import randint
import base64
from odoo import api, Command, fields, models, modules, _
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class AppCMIPerspectivasEjeEstrategico(models.Model):
    _name = 'sicpro.app.cmi.perspectivas.eje.estrategico'
    _order = "id asc"
    _description = 'Ejes Estratégicos del CMI'

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    descripcion = fields.Char(string="Descripción", required=True, )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, )
    anio = fields.Char(string="Año", required=True,
                       default=fields.Datetime.now().strftime("%Y"), )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
