# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresVacunacion(models.Model):
    _name = 'sicpro.app.trabajadores.vacunacion'
    _description = 'Vacunación de los trabajadores'
    _order = "fecha asc"

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    plaza_id = fields.Char(string="# Plaza", required=True)
    name = fields.Many2one('sicpro.app.trabajadores', required=False,)
    tipo_vacuna = fields.Char(string='Tipo de Vacuna', required=False)
    fecha = fields.Date(string='Fecha', required=False)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    @api.model
    def create(self, vals):
        vacunacion = super(TrabajadoresVacunacion, self).create(vals)
        trabajador = self.env['sicpro.app.trabajadores'].search([('plaza_id', '=', vals.get('plaza_id')), ])
        vacunacion['name'] = trabajador.id
        return vacunacion
