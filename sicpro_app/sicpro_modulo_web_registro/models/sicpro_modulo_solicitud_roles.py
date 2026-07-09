# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError


class PlanillaAccesoRoles(models.Model):
    _name = 'sicpro.modulo.solicitud.acceso.roles'
    _description = "Roles de la solicitud de Acceso"

    role_id = fields.Many2one(comodel_name="res.users.role",
                              string="Rol a Solicitar", required=True,
                              ondelete="cascade")
    user_id = fields.Many2one(comodel_name="res.users",
                              string="Usuario Asignado",
                              help="Usuario al que se le aplicará el rol tras la aprobación.")
    planilla_id = fields.Many2one(
        comodel_name="sicpro.modulo.solicitud.acceso",
        string="Planilla de Origen", required=True, ondelete="cascade")
    # Fechas y Control
    desde = fields.Date(string="Fecha Inicio",
                        default=fields.Date.context_today)
    hasta = fields.Date(string="Fecha Fin")
    aprobado = fields.Boolean(string="¿Aprobado?", default=False,
                              readonly=True)

    # Restricción de servidor (evita que se guarde data errónea)
    @api.constrains('desde', 'hasta')
    def _check_dates(self):
        for record in self:
            if record.desde and record.hasta and record.hasta < record.desde:
                raise ValidationError(
                    'Error en SICPRO: La fecha de fin no puede ser anterior a la de inicio.' + MSG_SOPORTE_SICPRO)

    # Validación en tiempo real para la interfaz
    @api.onchange('hasta')
    def _onchange_fecha_hasta(self):
        if self.desde and self.hasta and self.hasta < self.desde:
            return {'warning': {'title': "Fecha inválida",
                                'message': "La fecha de fin del rol no puede ser menor que la fecha de inicio.", }}

    def aprobar_rol(self):
        for item in self:
            item.aprobado = True
