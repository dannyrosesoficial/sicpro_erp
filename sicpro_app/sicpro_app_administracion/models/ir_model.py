# -*- coding: utf-8 -*-


from odoo import api, fields, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    modules_store = fields.Char(compute='_in_modules_store', string='Aplicación', store=True)

    @api.depends()
    def _in_modules_store(self):
        installed_modules = self.env['ir.module.module'].search([('state', '=', 'installed')])
        installed_names = set(installed_modules.mapped('name'))
        xml_ids = models.Model._get_external_ids(self)
        for field in self:
            module_names = set(
                xml_id.split('.')[0] for xml_id in xml_ids[field.id])
            field.modules_store = ", ".join(
                sorted(installed_names & module_names))
