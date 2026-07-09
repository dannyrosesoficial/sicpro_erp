# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ReunionesDespachosComentarios(models.Model):
    _name = 'sicpro.app.reuniones.despachos.comentarios'
    _description = 'Comentarios de los Despachos'

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    despacho_id = fields.Many2one('sicpro.app.reuniones.despachos', string='Despacho', required=True,)
    name = fields.Char(string='Comentarios', required=True)
    agenda_ids = fields.Many2one('sicpro.app.reuniones.despachos.agenda', string='Agenda/Puntos vinculada',
                                 required=True)
    registro_activo = fields.Integer(string='Registro_activo', required=False, )
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
