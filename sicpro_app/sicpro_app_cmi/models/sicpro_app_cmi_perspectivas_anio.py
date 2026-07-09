# -*- coding: utf-8 -*-


from random import randint
import base64
from odoo import api, Command, fields, models, modules, _
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class AppCMIPerspectivasAnios(models.Model):
    _name = 'sicpro.app.cmi.perspectivas.anios'
    _order = "id asc"
    _description = 'Años de las Perspectivas del CMI'

    def _default_image(self):
        image_path = modules.get_module_resource('sicpro_app_cmi', 'static/src/img', 'etecsaCi_300_8.png')
        return base64.b64encode(open(image_path, 'rb').read())

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char('Nombre', required=True, default='DVPE', readonly='1')
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True,)
    anio = fields.Char(string="Año", required=True,
                       default=fields.Datetime.now().strftime("%Y"), )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    image_128 = fields.Image("Image", max_width=128, max_height=128,
                             default=_default_image)

    _sql_constraints = [('anio_uniq', 'unique (anio)',
                         "El año introducido existe!, verifíquelo"), ]
