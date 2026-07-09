# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ReunionesDespachosParticipantes(models.Model):
    _name = 'sicpro.app.reuniones.despachos.participantes'
    _description = 'Participantes de los Despachos'

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    despacho_id = fields.Many2one('sicpro.app.reuniones.despachos', string='Despacho', required=True, readonly=True,)
    name = fields.Many2one('res.users', string='Trabajador', domain="[('tipo', '=', 'interno')]")
    email = fields.Char(string='Correo', related='name.email', store=True)
    cargo = fields.Char(string='Cargo', related='name.ocupacion_id.name.name', store=True)
    company_trabajador = fields.Many2one('res.company', string='Proceso Trabajador', related='name.company_id',
                                         store=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
