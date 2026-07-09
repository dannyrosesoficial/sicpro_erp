# -*- coding: utf-8 -*-

from odoo import models, fields


class NucleoReadonly(models.Model):
    _name = 'nucleo.sicpro.readonly'
    _description = 'Nucleo Readonly'

    name = fields.Char()

    def nucleo_readonly_check(self):
        # Código para extender la comprobación a todos los modelos:
        # Python:
        # readonly_admin = fields.Boolean(compute='_check_readonly_admin')
        #  def _check_readonly_admin(self):
        #      import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
        #          as nucleo_readonly_check
        #      for item in self:
        #          item.readonly_admin = nucleo_readonly_check.\
        #              NucleoReadonly.nucleo_readonly_check(self)
        # Xml:
        # <field name="readonly_admin" invisible="1"/>
        # Atributo para sustituir por: readonly="1"
        # attrs="{'readonly': [('readonly_admin', '!=', True)]}"
        grupo = self.env['res.users'].has_group \
            ('nucleo_sicpro_erp.grupo_readonly_admin')
        return grupo
