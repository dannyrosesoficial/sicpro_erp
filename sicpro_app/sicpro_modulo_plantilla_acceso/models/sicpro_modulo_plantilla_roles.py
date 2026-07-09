# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PlanillaAccesoRoles(models.Model):
    _name = 'sicpro.modulo.plantilla.acceso.roles'
    _description = "Roles de la plantilla de Acceso"

    role_id = fields.Many2one(comodel_name="sicpro.modulo.roles", required=True, string="Roles", ondelete="cascade")
    user_id = fields.Many2one(comodel_name="res.users", required=False, string="Usuarios",)
    planilla_id = fields.Many2one(comodel_name="sicpro.modulo.plantilla.acceso", required=True, string="Planilla",
                                  ondelete="cascade", )
    desde = fields.Date("Desde")
    hasta = fields.Date("Hasta")
    aprobado = fields.Boolean("Aprobado", default=False)

    # verifica que la fecha de fin del rol
    @api.depends('desde')
    @api.onchange('hasta')
    def _onchange_fecha_hasta(self):
        if self.hasta < self.desde:
            self.hasta = None
            raise UserError(_('La fecha de fin del rol no puede ser menor que la fecha de inicio, verifíquelo.'))

    def aprobar_rol(self):
        for item in self:
            item.aprobado = True

